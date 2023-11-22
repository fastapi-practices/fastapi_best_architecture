#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from pydantic.errors import EnumMemberError, WrongConstantError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from backend.app.common.exception.errors import BaseExceptionMixin
from backend.app.common.log import log
from backend.app.common.response.response_code import CustomResponseCode, StandardResponseCode
from backend.app.common.response.response_schema import ResponseModel, response_base
from backend.app.core.conf import settings


def register_exception(app: FastAPI):
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """
        全局HTTP异常处理

        :param request:
        :param exc:
        :return:
        """
        content = ResponseModel(code=exc.status_code, msg=exc.detail).dict()
        request.state.__request_http_exception__ = content  # 用于在中间件中获取异常信息
        return JSONResponse(
            status_code=StandardResponseCode.HTTP_400,
            content=content if settings.ENVIRONMENT == 'dev' else await response_base.fail(CustomResponseCode.HTTP_400),
            headers=exc.headers,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """
        数据验证异常处理

        :param request:
        :param exc:
        :return:
        """
        message = ''
        data = {}
        for raw_error in exc.raw_errors:
            raw_exc = raw_error.exc
            if isinstance(raw_exc, ValidationError):
                if hasattr(raw_exc, 'model'):
                    fields = raw_exc.model.__dict__.get('__fields__')
                    for field_key in fields.keys():
                        field_title = fields.get(field_key).field_info.title
                        data[field_key] = field_title if field_title else field_key
                # 处理特殊类型异常模板信息 -> backend/app/schemas/base.py: SCHEMA_ERROR_MSG_TEMPLATES
                for sub_raw_error in raw_exc.raw_errors:
                    sub_raw_exc = sub_raw_error.exc
                    if isinstance(sub_raw_exc, (EnumMemberError, WrongConstantError)):
                        if getattr(sub_raw_exc, 'code') == 'enum':
                            sub_raw_exc.__dict__['permitted'] = ', '.join(
                                repr(v.value)
                                for v in sub_raw_exc.enum_values  # type: ignore
                            )
                        else:
                            sub_raw_exc.__dict__['permitted'] = ', '.join(
                                repr(v)
                                for v in sub_raw_exc.permitted  # type: ignore
                            )
                # 处理异常信息
                for error in raw_exc.errors()[:1]:
                    field = str(error.get('loc')[-1])
                    msg = error.get('msg')
                    message += f'{data.get(field, field) if field != "__root__" else ""} {msg}' + '.'
            elif isinstance(raw_error.exc, json.JSONDecodeError):
                message += 'json解析失败'
        content = ResponseModel(
            code=StandardResponseCode.HTTP_422,
            msg='请求参数非法' if len(message) == 0 else f'请求参数非法: {message}',
            data={'errors': exc.errors()} if message == '' else None,
        ).dict()
        request.state.__request_validation_exception__ = content  # 用于在中间件中获取异常信息
        return JSONResponse(
            status_code=StandardResponseCode.HTTP_422,
            content=content if settings.ENVIRONMENT == 'dev' else await response_base.fail(CustomResponseCode.HTTP_422),
        )

    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception):
        """
        全局异常处理

        :param request:
        :param exc:
        :return:
        """
        if isinstance(exc, BaseExceptionMixin):
            return JSONResponse(
                status_code=StandardResponseCode.HTTP_400,
                content=ResponseModel(
                    code=exc.code,
                    msg=str(exc.msg),
                    data=exc.data if exc.data else None,
                ).dict(),
                background=exc.background,
            )

        elif isinstance(exc, AssertionError):
            return JSONResponse(
                status_code=StandardResponseCode.HTTP_500,
                content=ResponseModel(
                    code=StandardResponseCode.HTTP_500,
                    msg=','.join(exc.args)
                    if exc.args
                    else exc.__repr__()
                    if not exc.__repr__().startswith('AssertionError')
                    else exc.__doc__,
                ).dict()
                if settings.ENVIRONMENT == 'dev'
                else await response_base.fail(CustomResponseCode.HTTP_500),
            )

        else:
            import traceback

            log.error(f'未知异常: {exc}')
            log.error(traceback.format_exc())
            return JSONResponse(
                status_code=StandardResponseCode.HTTP_500,
                content=ResponseModel(code=500, msg=str(exc)).dict()
                if settings.ENVIRONMENT == 'dev'
                else await response_base.fail(CustomResponseCode.HTTP_500),
            )

    if settings.MIDDLEWARE_CORS:

        @app.exception_handler(StandardResponseCode.HTTP_500)
        async def cors_status_code_500_exception_handler(request, exc):
            """
            跨域 500 异常处理

            `Related issue <https://github.com/encode/starlette/issues/1175>`_

            :param request:
            :param exc:
            :return:
            """
            response = JSONResponse(
                status_code=exc.code if isinstance(exc, BaseExceptionMixin) else StandardResponseCode.HTTP_500,
                content=ResponseModel(code=exc.code, msg=exc.msg, data=exc.data).dict()
                if isinstance(exc, BaseExceptionMixin)
                else ResponseModel(code=StandardResponseCode.HTTP_500, msg=str(exc)).dict()
                if settings.ENVIRONMENT == 'dev'
                else await response_base.fail(CustomResponseCode.HTTP_500),
                background=exc.background if isinstance(exc, BaseExceptionMixin) else None,
            )
            origin = request.headers.get('origin')
            if origin:
                cors = CORSMiddleware(
                    app=app, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*']
                )
                response.headers.update(cors.simple_headers)
                has_cookie = 'cookie' in request.headers
                if cors.allow_all_origins and has_cookie:
                    response.headers['Access-Control-Allow-Origin'] = origin
                elif not cors.allow_all_origins and cors.is_allowed_origin(origin=origin):
                    response.headers['Access-Control-Allow-Origin'] = origin
                    response.headers.add_vary_header('Origin')
            return response
