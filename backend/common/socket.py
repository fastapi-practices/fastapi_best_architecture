#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socketio

from backend.common.log import log
from backend.core.conf import settings

sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_credentials=True,
    cors_allowed_origins=settings.CORS_ALLOWED_ORIGINS,
    namespaces=['/ws'],
)


@sio.event
async def connect(sid, environ):
    log.debug(sid, environ)
    await sio.emit('message', {'data': 'Welcome!'}, to=sid)


@sio.event
async def disconnect(sid):
    log.debug(sid)
