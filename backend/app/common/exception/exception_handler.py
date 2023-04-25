#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError, HTTPException
from pydantic import ValidationError
from starlette.responses import JSONResponse
from uvicorn.protocols.http.h11_impl import STATUS_PHRASES

from backend.app.common.exception.errors import BaseExceptionMixin
from backend.app.common.response.response_schema import response_base
from backend.app.core.conf import settings


def _get_exception_code(status_code):
    """
    获取返回状态码, OpenAPI, Uvicorn... 可用状态码基于 RFC 定义, 详细代码见下方链接

    `python 状态码标准支持 <https://github.com/python/cpython/blob/6e3cc72afeaee2532b4327776501eb8234ac787b/Lib/http
    /__init__.py#L7>`__

    `IANA 状态码注册表 <https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml>`__

    :param status_code:
    :return:
    """
    try:
        STATUS_PHRASES[status_code]
    except Exception:
        code = 400
    else:
        code = status_code
    return code


def register_exception(app: FastAPI):
    @app.exception_handler(HTTPException)
    def http_exception_handler(request: Request, exc: HTTPException):
        """
        全局HTTP异常处理

        :param request:
        :param exc:
        :return:
        """
        return JSONResponse(
            status_code=_get_exception_code(exc.status_code),
            content=response_base.fail(code=exc.status_code, msg=exc.detail),
            headers=exc.headers,
        )

    @app.exception_handler(Exception)
    def all_exception_handler(request: Request, exc):
        """
        全局异常处理

        :param request:
        :param exc:
        :return:
        """
        # 常规
        if isinstance(exc, RequestValidationError):
            message = ''
            data = {}
            for raw_error in exc.raw_errors:
                if isinstance(raw_error.exc, ValidationError):
                    exc = raw_error.exc
                    if hasattr(exc, 'model'):
                        fields = exc.model.__dict__.get('__fields__')
                        for field_key in fields.keys():
                            field_title = fields.get(field_key).field_info.title
                            data[field_key] = field_title if field_title else field_key
                    for error in exc.errors():
                        field = str(error.get('loc')[-1])
                        _msg = error.get('msg')
                        message += f'{data.get(field, field)} {_msg},'
                elif isinstance(raw_error.exc, json.JSONDecodeError):
                    message += 'json解析失败'
            return JSONResponse(
                status_code=422,
                content=response_base.fail(
                    msg='请求参数非法' if len(message) == 0 else f'请求参数非法:{message[:-1]}',
                    data={'errors': exc.errors()} if message == '' and settings.UVICORN_RELOAD is True else None,
                ),
            )

        # 自定义
        if isinstance(exc, BaseExceptionMixin):
            return JSONResponse(
                status_code=_get_exception_code(exc.code),
                content=response_base.fail(code=exc.code, msg=str(exc.msg), data=exc.data if exc.data else None),
            )

        else:
            return JSONResponse(
                status_code=500,
                content=response_base.fail(code=500, msg=str(exc))
                if settings.UVICORN_RELOAD
                else response_base.fail(code=500, msg='Internal Server Error'),
            )
