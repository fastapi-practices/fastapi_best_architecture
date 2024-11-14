#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socketio

from backend.app.task.conf import task_settings
from backend.common.log import log
from backend.common.security.jwt import jwt_authentication
from backend.core.conf import settings

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
