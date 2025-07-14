#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from starlette.concurrency import run_in_threadpool

from backend.app.task.celery import celery_app
from backend.common.socketio.server import sio


@sio.event
async def task_worker_status(sid, data):
    """任务 Worker 状态事件"""
    worker = await run_in_threadpool(celery_app.control.ping)
    await sio.emit('task_worker_status', worker, sid)
