#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any

from fastapi import HTTPException

from backend.app.common.response.response_code import CustomCode


class BaseExceptionMixin(Exception):
    code: int

    def __init__(self, *, msg: str = None, data: Any = None):
        self.msg = msg
        self.data = data


class HTTPError(HTTPException):
    def __init__(self, *, code: int, msg: Any = None, headers: dict[str, Any] | None = None):
        super().__init__(status_code=code, detail=msg, headers=headers)


class CustomError(BaseExceptionMixin):
    def __init__(self, *, error: CustomCode, data: Any = None):
        self.code = error.code
        super().__init__(msg=error.msg, data=data)


class RequestError(BaseExceptionMixin):
    code = 400

    def __init__(self, *, msg: str = 'Bad Request', data: Any = None):
        super().__init__(msg=msg, data=data)


class ForbiddenError(BaseExceptionMixin):
    code = 403

    def __init__(self, *, msg: str = 'Forbidden', data: Any = None):
        super().__init__(msg=msg, data=data)


class NotFoundError(BaseExceptionMixin):
    code = 404

    def __init__(self, *, msg: str = 'Not Found', data: Any = None):
        super().__init__(msg=msg, data=data)


class ServerError(BaseExceptionMixin):
    code = 500

    def __init__(self, *, msg: str = 'Internal Server Error', data: Any = None):
        super().__init__(msg=msg, data=data)


class GatewayError(BaseExceptionMixin):
    code = 502

    def __init__(self, *, msg: str = 'Bad Gateway', data: Any = None):
        super().__init__(msg=msg, data=data)


class AuthorizationError(BaseExceptionMixin):
    code = 401

    def __init__(self, *, msg: str = 'Permission denied', data: Any = None):
        super().__init__(msg=msg, data=data)


class TokenError(HTTPError):
    code = 401

    def __init__(self, *, msg: str = 'Not authenticated', headers: dict[str, Any] | None = None):
        super().__init__(code=self.code, msg=msg, headers=headers or {'WWW-Authenticate': 'Bearer'})
