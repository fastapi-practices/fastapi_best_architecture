#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from celery import Task
from sqlalchemy.exc import SQLAlchemyError

from backend.app.task.conf import task_settings
from backend.common.socketio.actions import task_notification


class TaskBase(Task):
    """任务基类"""

    autoretry_for = (SQLAlchemyError,)
    max_retries = task_settings.CELERY_TASK_MAX_RETRIES

    async def before_start(self, task_id, args, kwargs):
        await task_notification(msg=f'任务 {task_id} 开始执行')

    async def on_success(self, retval, task_id, args, kwargs):
        await task_notification(msg=f'任务 {task_id} 执行成功')

    async def on_failure(self, exc, task_id, args, kwargs, einfo):
        await task_notification(msg=f'任务 {task_id} 执行失败')
