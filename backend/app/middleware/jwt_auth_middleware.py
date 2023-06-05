#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any

from fastapi import Request, Response
from starlette.authentication import AuthenticationBackend, AuthenticationError
from starlette.requests import HTTPConnection
from starlette.responses import JSONResponse

from backend.app.common import jwt
from backend.app.common.exception.errors import TokenError
from backend.app.core.conf import settings
from backend.app.database.db_mysql import async_db_session


class _AuthenticationError(AuthenticationError):
    """重写内部认证错误类"""

    def __init__(self, *, code: int = None, msg: str = None, headers: dict[str, Any] | None = None):
        self.code = code
        self.msg = msg
        self.headers = headers


class JwtAuthMiddleware(AuthenticationBackend):
    """JWT 认证中间件"""

    @staticmethod
    def auth_exception_handler(conn: HTTPConnection, exc: Exception) -> Response:
        """覆盖内部认证错误处理"""
        code = getattr(exc, 'code', 500)
        msg = getattr(exc, 'msg', 'Internal Server Error')
        return JSONResponse(content={'code': code, 'msg': msg, 'data': None}, status_code=code)

    async def authenticate(self, request: Request):
        auth = request.headers.get('Authorization')
        if not auth:
            return

        scheme, token = auth.split()
        if scheme.lower() != 'bearer':
            return

        try:
            sub = await jwt.jwt_authentication(token)
            async with async_db_session() as db:
                user = await jwt.get_current_user(db, data=sub)
        except TokenError as exc:
            raise _AuthenticationError(code=exc.code, msg=exc.detail, headers=exc.headers)
        except Exception:
            import traceback

            raise _AuthenticationError(msg=traceback.format_exc() if settings.ENVIRONMENT == 'dev' else None)

        # 请注意，此返回使用非标准模式，所以在认证通过时，将丢失某些标准特性
        # 标准返回模式请查看：https://www.starlette.io/authentication/
        return auth, user
