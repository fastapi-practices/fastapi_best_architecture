#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

from asyncio import create_task
from typing import Any

from asgiref.sync import sync_to_async
from fastapi import Response
from starlette.datastructures import UploadFile
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from backend.app.admin.schema.opera_log import CreateOperaLogParam
from backend.app.admin.service.opera_log_service import opera_log_service
from backend.common.enums import OperaLogCipherType, StatusType
from backend.common.log import log
from backend.core.conf import settings
from backend.utils.encrypt import AESCipher, ItsDCipher, Md5Cipher
from backend.utils.trace_id import get_request_trace_id


class OperaLogMiddleware(BaseHTTPMiddleware):
    """操作日志中间件"""

    async def dispatch(self, request: Request, call_next: Any) -> Response:
        """
        处理请求并记录操作日志

        :param request: FastAPI 请求对象
        :param call_next: 下一个中间件或路由处理函数
        :return:
        """
        response = None
        path = request.url.path

        if path in settings.OPERA_LOG_PATH_EXCLUDE or not path.startswith(f'{settings.FASTAPI_API_V1_PATH}'):
            response = await call_next(request)
        else:
            method = request.method
            args = await self.get_request_args(request)
            args = await self.desensitization(args)

            # 执行请求
            elapsed = 0.0
            code = 200
            msg = 'Success'
            status = StatusType.enable
            error = None
            try:
                response = await call_next(request)
                elapsed = (time.perf_counter() - request.state.perf_time) * 1000
                for state in [
                    '__request_http_exception__',
                    '__request_validation_exception__',
                    '__request_assertion_error__',
                    '__request_custom_exception__',
                    '__request_all_unknown_exception__',
                    '__request_cors_500_exception__',
                ]:
                    exception = getattr(request.state, state, None)
                    if exception:
                        code = exception.get('code')
                        msg = exception.get('msg')
                        log.error(f'请求异常: {msg}')
                        break
            except Exception as e:
                log.error(f'请求异常: {str(e)}')
                code = getattr(e, 'code', code)  # 兼容 SQLAlchemy 异常用法
                msg = getattr(e, 'msg', msg)
                status = StatusType.disable
                error = e

            # 此信息只能在请求后获取
            _route = request.scope.get('route')
            summary = getattr(_route, 'summary', '')

            try:
                # 此信息来源于 JWT 认证中间件
                username = request.user.username
            except AttributeError:
                username = None

            # 日志记录
            log.debug(f'接口摘要：[{summary}]')
            log.debug(f'请求地址：[{request.state.ip}]')
            log.debug(f'请求参数：{args}')

            # 日志创建
            opera_log_in = CreateOperaLogParam(
                trace_id=get_request_trace_id(request),
                username=username,
                method=method,
                title=summary,
                path=path,
                ip=request.state.ip,
                country=request.state.country,
                region=request.state.region,
                city=request.state.city,
                user_agent=request.state.user_agent,
                os=request.state.os,
                browser=request.state.browser,
                device=request.state.device,
                args=args,
                status=status,
                code=str(code),
                msg=msg,
                cost_time=elapsed,  # 可能和日志存在微小差异（可忽略）
                opera_time=request.state.start_time,
            )
            create_task(opera_log_service.create(obj=opera_log_in))  # noqa: ignore

            # 错误抛出
            if error:
                raise error from None

        return response

    @staticmethod
    async def get_request_args(request: Request) -> dict[str, Any]:
        """
        获取请求参数

        :param request: FastAPI 请求对象
        :return:
        """
        args = {}
        query_params = dict(request.query_params)
        if query_params:
            args['query_params'] = query_params
        path_params = request.path_params
        if path_params:
            args['path_params'] = path_params
        # Tip: .body() 必须在 .form() 之前获取
        # https://github.com/encode/starlette/discussions/1933
        content_type = request.headers.get('Content-Type', '').split(';')
        body_data = await request.body()
        if body_data:
            # 注意：非 json 数据默认使用 body 作为键
            if 'application/json' not in content_type:
                args['data'] = str(body_data)
            else:
                json_data = await request.json()
                if isinstance(json_data, dict):
                    args['json'] = json_data
                else:
                    args['data'] = str(body_data)
        form_data = await request.form()
        if len(form_data) > 0:
            for k, v in form_data.items():
                if isinstance(v, UploadFile):
                    form_data = {k: v.filename}
                else:
                    form_data = {k: v}
            if 'multipart/form-data' not in content_type:
                args['x-www-form-urlencoded'] = form_data
            else:
                args['form-data'] = form_data

        return args

    @staticmethod
    @sync_to_async
    def desensitization(args: dict[str, Any]) -> dict[str, Any] | None:
        """
        脱敏处理

        :param args: 需要脱敏的参数字典
        :return:
        """
        if not args:
            return None

        encrypt_type = settings.OPERA_LOG_ENCRYPT_TYPE
        encrypt_key_include = settings.OPERA_LOG_ENCRYPT_KEY_INCLUDE
        encrypt_secret_key = settings.OPERA_LOG_ENCRYPT_SECRET_KEY

        for key, value in args.items():
            if key in encrypt_key_include:
                match encrypt_type:
                    case OperaLogCipherType.aes:
                        args[key] = (AESCipher(encrypt_secret_key).encrypt(value)).hex()
                    case OperaLogCipherType.md5:
                        args[key] = Md5Cipher.encrypt(value)
                    case OperaLogCipherType.itsdangerous:
                        args[key] = ItsDCipher(encrypt_secret_key).encrypt(value)
                    case OperaLogCipherType.plan:
                        pass
                    case _:
                        args[key] = '******'
        return args
