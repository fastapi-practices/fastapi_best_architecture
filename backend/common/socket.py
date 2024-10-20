#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socketio

from backend.core.conf import settings

sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=settings.CORS_ALLOWED_ORIGINS,
    cors_credentials=True,
)


@sio.event
async def connect(sid, environ):
    print(sid, environ)


@sio.event
async def disconnect(sid):
    print(sid)

@sio.event
async def message(sid, data):
    print(f'Message from {sid}: {data}')
    await sio.emit('message', data)
