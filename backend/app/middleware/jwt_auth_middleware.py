#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from starlette.authentication import AuthenticationBackend
from fastapi import Request

from backend.app.common import jwt
from backend.app.database.db_mysql import async_db_session


class JwtAuthMiddleware(AuthenticationBackend):
    """JWT 认证中间件"""

    async def authenticate(self, request: Request):
        auth = request.headers.get('Authorization')
        if not auth:
            return

        scheme, token = auth.split()
        if scheme.lower() != 'bearer':
            return

        sub = await jwt.jwt_authentication(token)

        async with async_db_session() as db:
            user = await jwt.get_current_user(db, data=sub)

        return auth, user
