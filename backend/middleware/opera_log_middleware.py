#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from asyncio import create_task

from asgiref.sync import sync_to_async
from fastapi import Response
from starlette.datastructures import UploadFile
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from backend.app.admin.schema.opera_log import CreateOperaLogParam
from backend.app.admin.service.opera_log_service import OperaLogService
from backend.common.enums import OperaLogCipherType
from backend.common.log import log
from backend.core.conf import settings
from backend.utils.encrypt import AESCipher, ItsDCipher, Md5Cipher
from backend.utils.request_parse import parse_ip_info, parse_user_agent_info
from backend.utils.timezone import timezone


class OperaLogMiddleware(BaseHTTPMiddleware):
    """操作日志中间件"""

    async def dispatch(self, request: Request, call_next) -> Response:
        # 排除记录白名单
        path = request.url.path
        if path in settings.OPERA_LOG_EXCLUDE or not path.startswith(f'{settings.API_V1_STR}'):
            return await call_next(request)

        # 请求解析
        user_agent, device, os, browser = await parse_user_agent_info(request)
        ip, country, region, city = await parse_ip_info(request)
        try:
            # 此信息依赖于 jwt 中间件
            username = request.user.username
        except AttributeError:
            username = None
        method = request.method
        router = request.scope.get('route')
        summary = getattr(router, 'summary', None) or ''
        args = await self.get_request_args(request)
        args = await self.desensitization(args)

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
        code, msg, status, err, response = await self.execute_request(request, call_next)
        end_time = timezone.now()
        cost_time = (end_time - start_time).total_seconds() * 1000.0

        # 日志创建
        opera_log_in = CreateOperaLogParam(
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
        create_task(OperaLogService.create(obj_in=opera_log_in))  # noqa: ignore

        # 错误抛出
        if err:
            raise err from None

        return response

    async def execute_request(self, request: Request, call_next) -> tuple:
        """执行请求"""
        err = None
        response = None
        try:
            response = await call_next(request)
            code, msg, status = await self.request_exception_handler(request)
        except Exception as e:
            log.exception(e)
            # code 处理包含 SQLAlchemy 和 Pydantic
            code = getattr(e, 'code', None) or 500
            msg = getattr(e, 'msg', None) or 'Internal Server Error'
            status = 0
            err = e

        return str(code), msg, status, err, response

    @staticmethod
    @sync_to_async
    def request_exception_handler(request: Request) -> tuple:
        """请求异常处理器"""
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
        """获取请求参数"""
        args = dict(request.query_params)
        args.update(request.path_params)
        # Tip: .body() 必须在 .form() 之前获取
        # https://github.com/encode/starlette/discussions/1933
        body_data = await request.body()
        form_data = await request.form()
        if len(form_data) > 0:
            args.update({k: v.filename if isinstance(v, UploadFile) else v for k, v in form_data.items()})
        else:
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
        """
        脱敏处理

        :param args:
        :return:
        """
        if not args:
            args = None
        else:
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
        return args
