#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.common.socketio.server import sio


async def task_notification(msg: str):
    """
    任务通知

    :param msg:
    :return:
    """
    await sio.emit('task_notification', {'msg': msg})
