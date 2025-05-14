#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socketio

from backend.common.log import log
from backend.common.security.jwt import jwt_authentication
from backend.core.conf import settings
from backend.database.redis import redis_client

# Examples of creating a Socket.IO server
sio = socketio.AsyncServer(
    # _Other Organiser
    client_manager=socketio.AsyncRedisManager(
        f'redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:'
        f'{settings.REDIS_PORT}/{settings.CELERY_BROKER_REDIS_DATABASE}'
    )
    if settings.CELERY_BROKER == 'redis'
    else socketio.AsyncAioPikaManager(
        (
            f'amqp://{settings.CELERY_RABBITMQ_USERNAME}:{settings.CELERY_RABBITMQ_PASSWORD}@'
            f'{settings.CELERY_RABBITMQ_HOST}:{settings.CELERY_RABBITMQ_PORT}'
        )
    ),
    async_mode='asgi',
    cors_allowed_origins=settings.CORS_ALLOWED_ORIGINS,
    cors_credentials=True,
    namespaces=['/ws'],
)


@sio.event
async def connect(sid, environ, auth):
    """Process WebSocket connection events"""
    if not auth:
        log.error('WebSocket connection failed: no authorization')
        return False

    session_uuid = auth.get('session_uuid')
    token = auth.get('token')
    if not token or not session_uuid:
        log.error('WebSocket connection failed: authorization failed, check')
        return False

    # Unauthorized direct
    if token == settings.WS_NO_AUTH_MARKER:
        await redis_client.sadd(settings.TOKEN_ONLINE_REDIS_PREFIX, session_uuid)
        return True

    try:
        await jwt_authentication(token)
    except Exception as e:
        log.info(f'WebSocket Connection Failed: {str(e)}')
        return False

    await redis_client.sadd(settings.TOKEN_ONLINE_REDIS_PREFIX, session_uuid)
    return True


@sio.event
async def disconnect(sid: str) -> None:
    """Process WebSocket disconnection events"""
    await redis_client.spop(settings.TOKEN_ONLINE_REDIS_PREFIX)
