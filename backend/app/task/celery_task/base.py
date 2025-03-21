#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any

from celery import Task
from sqlalchemy.exc import SQLAlchemyError

from backend.app.task.conf import task_settings
from backend.common.socketio.actions import task_notification


class TaskBase(Task):
    """Celery 任务基类"""

    autoretry_for = (SQLAlchemyError,)
    max_retries = task_settings.CELERY_TASK_MAX_RETRIES

    async def before_start(self, task_id: str, args, kwargs) -> None:
        """
        任务开始前执行钩子

        :param task_id: 任务 ID
        :return:
        """
        await task_notification(msg=f'任务 {task_id} 开始执行')

    async def on_success(self, retval: Any, task_id: str, args, kwargs) -> None:
        """
        任务成功后执行钩子

        :param retval: 任务返回值
        :param task_id: 任务 ID
        :return:
        """
        await task_notification(msg=f'任务 {task_id} 执行成功')

    async def on_failure(self, exc: Exception, task_id: str, args, kwargs, einfo) -> None:
        """
        任务失败后执行钩子

        :param exc: 异常对象
        :param task_id: 任务 ID
        :param einfo: 异常信息
        :return:
        """
        await task_notification(msg=f'任务 {task_id} 执行失败')
