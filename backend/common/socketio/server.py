#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socketio

from backend.app.task.conf import task_settings
from backend.common.log import log
from backend.common.security.jwt import jwt_authentication
from backend.core.conf import settings
from backend.database.redis import redis_client

# 创建 Socket.IO 服务器实例
sio = socketio.AsyncServer(
    # 集成 Celery 实现消息订阅
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
    """处理 WebSocket 连接事件"""
    if not auth:
        log.error('WebSocket 连接失败：无授权')
        return False

    session_uuid = auth.get('session_uuid')
    token = auth.get('token')
    if not token or not session_uuid:
        log.error('WebSocket 连接失败：授权失败，请检查')
        return False

    # 免授权直连
    if token == settings.WS_NO_AUTH_MARKER:
        await redis_client.sadd(settings.TOKEN_ONLINE_REDIS_PREFIX, session_uuid)
        return True

    try:
        await jwt_authentication(token)
    except Exception as e:
        log.info(f'WebSocket 连接失败：{str(e)}')
        return False

    await redis_client.sadd(settings.TOKEN_ONLINE_REDIS_PREFIX, session_uuid)
    return True


@sio.event
async def disconnect(sid: str) -> None:
    """处理 WebSocket 断开连接事件"""
    await redis_client.spop(settings.TOKEN_ONLINE_REDIS_PREFIX)
