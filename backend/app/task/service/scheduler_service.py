#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from celery.exceptions import NotRegistered
from celery.result import AsyncResult

from backend.app.task.celery import celery_app
from backend.common.exception import errors


class TaskSchedulerService:
    @staticmethod
    def revoke(*, task_id: str) -> None:
        """
        撤销指定的任务

        :param task_id: 任务 UUID
        :return:
        """
        try:
            result = AsyncResult(id=task_id, app=celery_app)
        except NotRegistered:
            raise errors.NotFoundError(msg='任务不存在')
        result.revoke(terminate=True)

    @staticmethod
    def execute(*, pk: int) -> str:
        """
        执行任务

        :param pk: 任务调度 ID
        :return:
        """
        task: AsyncResult = celery_app.send_task()
        return task.task_id


task_scheduler_service: TaskSchedulerService = TaskSchedulerService()
