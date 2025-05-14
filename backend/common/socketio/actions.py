#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.common.socketio.server import sio


async def task_notification(msg: str):
    """
    Job announcement

    :param msg: notification information
    :return:
    """
    await sio.emit('task_notification', {'msg': msg})
