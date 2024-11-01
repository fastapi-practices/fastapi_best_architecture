#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socketio

from backend.common.log import log
from backend.common.security.jwt import jwt_authentication
from backend.core.conf import settings

sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=settings.CORS_ALLOWED_ORIGINS,
    cors_credentials=True,
    namespaces=['/ws'],
)


@sio.event
async def connect(sid, environ, auth):
    if not auth:
        print('ws 连接失败：无授权')
        return False

    token = auth.get('token')
    if not token:
        print('ws 连接失败：无 token 授权')
        return False

    if token == 'internal':
        return True

    try:
        await jwt_authentication(token)
    except Exception as e:
        log.info(f'ws 连接失败：{e}')
        return False

    return True


@sio.event
async def disconnect(sid):
    pass
