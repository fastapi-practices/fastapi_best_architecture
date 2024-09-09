#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any

from fastapi import Request, Response
from fastapi.security.utils import get_authorization_scheme_param
from pydantic_core import from_json
from starlette.authentication import AuthCredentials, AuthenticationBackend, AuthenticationError
from starlette.requests import HTTPConnection

from backend.app.admin.schema.user import CurrentUserIns
from backend.common.exception.errors import TokenError
from backend.common.log import log
from backend.common.security import jwt
from backend.core.conf import settings
from backend.database.db_mysql import async_db_session
from backend.database.db_redis import redis_client
from backend.utils.serializers import MsgSpecJSONResponse, select_as_dict


class _AuthenticationError(AuthenticationError):
    """重写内部认证错误类"""

    def __init__(self, *, code: int = None, msg: str = None, headers: dict[str, Any] | None = None):
        self.code = code
        self.msg = msg
        self.headers = headers


class JwtAuthMiddleware(AuthenticationBackend):
    """JWT 认证中间件"""

    @staticmethod
    def auth_exception_handler(conn: HTTPConnection, exc: _AuthenticationError) -> Response:
        """覆盖内部认证错误处理"""
        return MsgSpecJSONResponse(content={'code': exc.code, 'msg': exc.msg, 'data': None}, status_code=exc.code)

    async def authenticate(self, request: Request) -> tuple[AuthCredentials, CurrentUserIns] | None:
        token = request.headers.get('Authorization')
        if not token:
            return

        if request.url.path in settings.TOKEN_REQUEST_PATH_EXCLUDE:
            return

        scheme, token = get_authorization_scheme_param(token)
        if scheme.lower() != 'bearer':
            return

        try:
            sub = await jwt.jwt_authentication(token)
            cache_user = await redis_client.get(f'{settings.JWT_USER_REDIS_PREFIX}:{sub}')
            if not cache_user:
                async with async_db_session() as db:
                    current_user = await jwt.get_current_user(db, sub)
                    user = CurrentUserIns(**select_as_dict(current_user))
                    await redis_client.setex(
                        f'{settings.JWT_USER_REDIS_PREFIX}:{sub}',
                        settings.JWT_USER_REDIS_EXPIRE_SECONDS,
                        user.model_dump_json(),
                    )
            else:
                # TODO: 在恰当的时机，应替换为使用 model_validate_json
                # https://docs.pydantic.dev/latest/concepts/json/#partial-json-parsing
                user = CurrentUserIns.model_validate(from_json(cache_user, allow_partial=True))
        except TokenError as exc:
            raise _AuthenticationError(code=exc.code, msg=exc.detail, headers=exc.headers)
        except Exception as e:
            log.error(f'JWT 授权异常：{e}')
            raise _AuthenticationError(code=getattr(e, 'code', 500), msg=getattr(e, 'msg', 'Internal Server Error'))

        # 请注意，此返回使用非标准模式，所以在认证通过时，将丢失某些标准特性
        # 标准返回模式请查看：https://www.starlette.io/authentication/
        return AuthCredentials(['authenticated']), user
