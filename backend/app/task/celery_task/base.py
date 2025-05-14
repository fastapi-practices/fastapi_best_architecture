#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio

from typing import Any

from celery import Task
from sqlalchemy.exc import SQLAlchemyError

from backend.app.task.conf import task_settings
from backend.common.socketio.actions import task_notification


class TaskBase(Task):
    """Celery Job Base Category"""

    autoretry_for = (SQLAlchemyError,)
    max_retries = task_settings.CELERY_TASK_MAX_RETRIES

    async def before_start(self, task_id: str, args, kwargs) -> None:
        """
        A hook before the mission starts

        :param task_id: task ID
        :return:
        """
        await task_notification(msg=f'mission {task_id} start')

    async def on_success(self, retval: Any, task_id: str, args, kwargs) -> None:
        """
        After mission success, execute hooks

        :param retval: task return value
        :param task_id: task ID
        :return:
        """
        await task_notification(msg=f'task {task_id} successfully executed')

    def on_failure(self, exc: Exception, task_id: str, args, kwargs, einfo) -> None:
        """
        Execute hooks after mission failure

        :param exc: abnormal object
        :param task_id: task ID
        :param einfo: abnormal information
        :return:
        """
        loop = asyncio.get_event_loop()
        loop.create_task(task_notification(msg=f'task {task_id} failed'))
