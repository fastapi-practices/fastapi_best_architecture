#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Any

from asgiref.sync import sync_to_async
from fastapi import UploadFile
from starlette.background import BackgroundTask
from starlette.requests import Request
from starlette.types import ASGIApp, Scope, Receive, Send

from backend.app.common.enums import OperaLogCipherType
from backend.app.common.log import log
from backend.app.core.conf import settings
from backend.app.schemas.opera_log import CreateOperaLog
from backend.app.services.opera_log_service import OperaLogService
from backend.app.utils.encrypt import AESCipher, Md5Cipher
from backend.app.utils.request_parse import parse_user_agent_info, parse_ip_info


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
        start_time = datetime.now()
        code, msg, status, err = await self.execute_request(request, send)
        end_time = datetime.now()
        cost_time = (end_time - start_time).total_seconds() * 1000.0

        router = request.scope.get('route')
        summary = getattr(router, 'summary', '')
        args.update(request.path_params)
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
        # 预置响应信息
        code: int = 200
        msg: str = 'Success'
        status: bool = True
        err: Any = None
        try:
            # 详见 https://github.com/tiangolo/fastapi/discussions/8385#discussioncomment-6117967
            async def wrapped_rcv_gen():
                async for _ in request.stream():
                    yield {'type': 'http.request', 'body': await request.body()}
                    async for message in request.receive:  # type: ignore
                        # assert message['type'] == 'http.response.body'
                        # body = message.get('body', b'')
                        # if body:
                        #     yield body
                        yield message

            wrapped_rcv = wrapped_rcv_gen().__anext__
            await self.app(request.scope, wrapped_rcv, send)
        except Exception as e:
            log.exception(e)
            code = getattr(e, 'code', '500')
            msg = getattr(e, 'msg', 'Internal Server Error')
            status = False
            err = e

        return code, msg, status, err

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
                args.update(json_data)
        return args

    @staticmethod
    @sync_to_async
    def desensitization(args: dict):
        if len(args) > 0:
            match settings.OPERA_LOG_ENCRYPT:
                case OperaLogCipherType.aes:
                    for key in args.keys():
                        if key in settings.OPERA_LOG_ENCRYPT_INCLUDE:
                            args[key] = (
                                AESCipher(settings.OPERA_LOG_ENCRYPT_SECRET_KEY).encrypt(
                                    bytes(args[key], encoding='utf-8')
                                )
                            ).hex()
                case OperaLogCipherType.md5:
                    for key in args.keys():
                        if key in settings.OPERA_LOG_ENCRYPT_INCLUDE:
                            args[key] = Md5Cipher.encrypt(args[key])
                case OperaLogCipherType.plan:
                    pass
                case _:
                    for key in args.keys():
                        if key in settings.OPERA_LOG_ENCRYPT_INCLUDE:
                            args[key] = '******'
        return args if len(args) > 0 else None
