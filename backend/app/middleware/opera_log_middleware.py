#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any, AsyncGenerator

from asgiref.sync import sync_to_async
from starlette.background import BackgroundTask
from starlette.datastructures import UploadFile
from starlette.requests import Request
from starlette.types import ASGIApp, Receive, Scope, Send

from backend.app.common.enums import OperaLogCipherType
from backend.app.common.log import log
from backend.app.core.conf import settings
from backend.app.schemas.opera_log import CreateOperaLog
from backend.app.services.opera_log_service import OperaLogService
from backend.app.utils.encrypt import AESCipher, ItsDCipher, Md5Cipher
from backend.app.utils.request_parse import parse_ip_info, parse_user_agent_info
from backend.app.utils.timezone import timezone


class OperaLogMiddleware:
    """操作日志中间件"""

    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope['type'] != 'http':
            await self.app(scope, receive, send)
            return

        request = Request(scope=scope, receive=receive)

        # 排除记录白名单
        path = request.url.path
        if path in settings.OPERA_LOG_EXCLUDE or not path.startswith(f'{settings.API_V1_STR}'):
            await self.app(scope, receive, send)
            return

        # 请求信息解析
        user_agent, device, os, browser = await parse_user_agent_info(request)
        ip, country, region, city = await parse_ip_info(request)
        try:
            # 此信息依赖于 jwt 中间件
            username = request.user.username
        except AttributeError:
            username = None
        method = request.method
        args = await self.get_request_args(request)
        router = request.scope.get('route')
        summary = getattr(router, 'summary', None) or ''
        args.update(request.path_params)

        # 设置附加请求信息
        request.state.ip = ip
        request.state.country = country
        request.state.region = region
        request.state.city = city
        request.state.user_agent = user_agent
        request.state.os = os
        request.state.browser = browser
        request.state.device = device

        # 执行请求
        start_time = timezone.now()
        code, msg, status, err = await self.execute_request(request, send)
        end_time = timezone.now()
        cost_time = (end_time - start_time).total_seconds() * 1000.0

        # 脱敏处理
        args = await self.desensitization(args)

        # 日志创建
        opera_log_in = CreateOperaLog(
            username=username,
            method=method,
            title=summary,
            path=path,
            ip=ip,
            country=country,
            region=region,
            city=city,
            user_agent=user_agent,
            os=os,
            browser=browser,
            device=device,
            args=args,
            status=status,
            code=code,
            msg=msg,
            cost_time=cost_time,
            opera_time=start_time,
        )
        back = BackgroundTask(OperaLogService.create, obj_in=opera_log_in)
        await back()

        # 错误抛出
        if err:
            raise err from None

    async def execute_request(self, request: Request, send: Send) -> tuple:
        err: Any = None
        try:
            # 详见 https://github.com/tiangolo/fastapi/discussions/8385#discussioncomment-6117967
            async def wrapped_rcv_gen() -> AsyncGenerator:
                async for _ in request.stream():
                    yield {'type': 'http.request', 'body': await request.body()}
                    async for message in request.receive:  # type: ignore
                        yield message

            wrapped_rcv = wrapped_rcv_gen().__anext__
            await self.app(request.scope, wrapped_rcv, send)
            code, msg, status = await self.exception_middleware_handler(request)
        except Exception as e:
            log.exception(e)
            # code 处理包含 SQLAlchemy 和 Pydantic
            code = getattr(e, 'code', None) or 500
            msg = getattr(e, 'msg', None) or 'Internal Server Error'
            status = 0
            err = e

        return str(code), msg, status, err

    @staticmethod
    @sync_to_async
    def exception_middleware_handler(request: Request) -> tuple:
        # 预置响应信息
        code = 200
        msg = 'Success'
        status = 1
        try:
            http_exception = request.state.__request_http_exception__
        except AttributeError:
            pass
        else:
            code = http_exception.get('code', 500)
            msg = http_exception.get('msg', 'Internal Server Error')
            status = 0
        try:
            validation_exception = request.state.__request_validation_exception__
        except AttributeError:
            pass
        else:
            code = validation_exception.get('code', 400)
            msg = validation_exception.get('msg', 'Bad Request')
            status = 0
        return code, msg, status

    @staticmethod
    async def get_request_args(request: Request) -> dict:
        args = dict(request.query_params)
        form_data = await request.form()
        if len(form_data) > 0:
            args.update({k: v.filename if isinstance(v, UploadFile) else v for k, v in form_data.items()})
        else:
            body_data = await request.body()
            if body_data:
                json_data = await request.json()
                if not isinstance(json_data, dict):
                    json_data = {
                        f'{type(json_data)}_to_dict_data': json_data.decode('utf-8')
                        if isinstance(json_data, bytes)
                        else json_data
                    }
                args.update(json_data)
        return args

    @staticmethod
    @sync_to_async
    def desensitization(args: dict) -> dict | None:
        if len(args) > 0:
            match settings.OPERA_LOG_ENCRYPT:
                case OperaLogCipherType.aes:
                    for key in args.keys():
                        if key in settings.OPERA_LOG_ENCRYPT_INCLUDE:
                            args[key] = (AESCipher(settings.OPERA_LOG_ENCRYPT_SECRET_KEY).encrypt(args[key])).hex()
                case OperaLogCipherType.md5:
                    for key in args.keys():
                        if key in settings.OPERA_LOG_ENCRYPT_INCLUDE:
                            args[key] = Md5Cipher.encrypt(args[key])
                case OperaLogCipherType.itsdangerous:
                    for key in args.keys():
                        if key in settings.OPERA_LOG_ENCRYPT_INCLUDE:
                            args[key] = ItsDCipher(settings.OPERA_LOG_ENCRYPT_SECRET_KEY).encrypt(args[key])
                case OperaLogCipherType.plan:
                    pass
                case _:
                    for key in args.keys():
                        if key in settings.OPERA_LOG_ENCRYPT_INCLUDE:
                            args[key] = '******'
        return args if len(args) > 0 else None
