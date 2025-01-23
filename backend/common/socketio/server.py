#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socketio

from backend.app.task.conf import task_settings
from backend.common.log import log
from backend.common.security.jwt import jwt_authentication
from backend.core.conf import settings
from backend.database.redis import redis_client

sio = socketio.AsyncServer(
    # 此配置是为了集成 celery 实现消息订阅，如果你不使用 celery，可以直接删除此配置，不会造成任何影响
    client_manager=socketio.AsyncRedisManager(
        f'redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:'
        f'{settings.REDIS_PORT}/{task_settings.CELERY_BROKER_REDIS_DATABASE}'
    )
    if task_settings.CELERY_BROKER == 'redis'
    else socketio.AsyncAioPikaManager(
        (
            f'amqp://{task_settings.RABBITMQ_USERNAME}:{task_settings.RABBITMQ_PASSWORD}@'
            f'{task_settings.RABBITMQ_HOST}:{task_settings.RABBITMQ_PORT}'
        )
    ),
    async_mode='asgi',
    cors_allowed_origins=settings.CORS_ALLOWED_ORIGINS,
    cors_credentials=True,
    namespaces=['/ws'],
)


@sio.event
async def connect(sid, environ, auth):
    """当客户端连接时触发"""
    if not auth:
        log.error('ws 连接失败：无授权')
        return False

    session_uuid = auth.get('session_uuid')
    token = auth.get('token')
    if not token or not session_uuid:
        log.error('ws 连接失败：授权失败，请检查')
        return False

    # 免授权直连
    if token == settings.WS_NO_AUTH_MARKER:
        await redis_client.sadd(settings.TOKEN_ONLINE_REDIS_PREFIX, session_uuid)
        return True

    try:
        await jwt_authentication(token)
    except Exception as e:
        log.info(f'ws 连接失败：{e}')
        return False

    await redis_client.sadd(settings.TOKEN_ONLINE_REDIS_PREFIX, session_uuid)
    return True


@sio.event
async def disconnect(sid):
    """当客户端断开连接时触发"""
    await redis_client.spop(settings.TOKEN_ONLINE_REDIS_PREFIX)
