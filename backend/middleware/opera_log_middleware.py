#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from asyncio import create_task
from typing import Any

from asgiref.sync import sync_to_async
from fastapi import Response
from starlette.datastructures import UploadFile
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from backend.app.admin.schema.opera_log import CreateOperaLogParam
from backend.app.admin.service.opera_log_service import opera_log_service
from backend.common.dataclasses import RequestCallNext
from backend.common.enums import OperaLogCipherType, StatusType
from backend.common.log import log
from backend.core.conf import settings
from backend.utils.encrypt import AESCipher, ItsDCipher, Md5Cipher
from backend.utils.timezone import timezone
from backend.utils.trace_id import get_request_trace_id


class OperaLogMiddleware(BaseHTTPMiddleware):
    """Operation log middle"""

    async def dispatch(self, request: Request, call_next: Any) -> Response:
        """
        Processing requests and recording operations logs

        :param request: FastAPI
        :param call_text: next intermediate or route processing function
        :return:
        """
        # Exclude the white list of records
        path = request.url.path
        if path in settings.OPERA_LOG_PATH_EXCLUDE or not path.startswith(f'{settings.FASTAPI_API_V1_PATH}'):
            return await call_next(request)

        # Request Parsing
        try:
            # this information depends on the jwt middle
            username = request.user.username
        except AttributeError:
            username = None
        method = request.method
        args = await self.get_request_args(request)
        args = await self.desensitization(args)

        # Enforcement of requests
        start_time = timezone.now()
        request_next = await self.execute_request(request, call_next)
        end_time = timezone.now()
        cost_time = round((end_time - start_time).total_seconds() * 1000.0, 3)

        # This information can only be obtained after request
        _route = request.scope.get('route')
        summary = getattr(_route, 'summary', None) or ''

        # Log Creation
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
            status=request_next.status,
            code=request_next.code,
            msg=request_next.msg,
            cost_time=cost_time,
            opera_time=start_time,
        )
        create_task(opera_log_service.create(obj=opera_log_in))  # noqa: ignore

        # Error Throwing
        if request_next.err:
            raise request_next.err from None

        return request_next.response

    async def execute_request(self, request: Request, call_next: Any) -> RequestCallNext:
        """
        Execute requests and handle anomalies

        :param request: FastAPI
        :param call_text: next intermediate or route processing function
        :return:
        """
        code = 200
        msg = 'Success'
        status = StatusType.enable
        err = None
        response = None
        try:
            response = await call_next(request)
            code, msg = self.request_exception_handler(request, code, msg)
        except Exception as e:
            log.error(f'request abnormal: {str(e)}')
            # code process containing SQLAlchemy and Pydantic
            code = getattr(e, 'code', code)
            msg = getattr(e, 'msg', msg)
            status = StatusType.disable
            err = e

        return RequestCallNext(code=str(code), msg=msg, status=status, err=err, response=response)

    @staticmethod
    def request_exception_handler(request: Request, code: int, msg: str) -> tuple[str, str]:
        """
        Request anomaly processor

        :param request: FastAPI
        :param code: error code
        :param msg: error message
        :return:
        """
        exception_states = [
            '__request_http_exception__',
            '__request_validation_exception__',
            '__request_assertion_error__',
            '__request_custom_exception__',
            '__request_all_unknown_exception__',
            '__request_cors_500_exception__',
        ]
        for state in exception_states:
            exception = getattr(request.state, state, None)
            if exception:
                code = exception.get('code')
                msg = exception.get('msg')
                log.error(f'request abnormal: {msg}')
                break
        return code, msg

    @staticmethod
    async def get_request_args(request: Request) -> dict[str, Any]:
        """
        Get Request Parameters

        :param request: FastAPI
        :return:
        """
        args = dict(request.query_params)
        args.update(request.path_params)
        # Tip: .body() must obtain before .form()
        # https://github.com/encode/starlette/discussions/1933
        body_data = await request.body()
        form_data = await request.form()
        if len(form_data) > 0:
            args.update({k: v.filename if isinstance(v, UploadFile) else v for k, v in form_data.items()})
        elif body_data:
            content_type = request.headers.get('Content-Type', '').split(';')
            if 'application/json' in content_type:
                json_data = await request.json()
                if isinstance(json_data, dict):
                    args.update(json_data)
                else:
                    # note: the non-dictionaries data default using body as key
                    args.update({'body': str(body_data)})
            else:
                args.update({'body': str(body_data)})
        return args

    @staticmethod
    @sync_to_async
    def desensitization(args: dict[str, Any]) -> dict[str, Any] | None:
        """
        Sensitization

        :param args: desensitive numerics required
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
