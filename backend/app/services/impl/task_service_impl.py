#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from celery.exceptions import BackendGetMetaError, NotRegistered
from celery.result import AsyncResult

from backend.app.common.celery import celery_app
from backend.app.common.exception.errors import NotFoundError
from backend.app.services.task_service import TaskServiceABC


class TaskServiceImpl(TaskServiceABC):
    """
    任务服务实现类
    """

    def get(self, pk: str) -> AsyncResult | None:
        try:
            result = celery_app.AsyncResult(pk)
        except (BackendGetMetaError, NotRegistered):
            raise NotFoundError(msg='任务不存在')
        if result.failed():
            return None
        return result

    def get_task_list(self) -> list:
        task_list = []
        tasks = celery_app.tasks
        for key, value in tasks.items():
            if not key.startswith('celery.'):
                filtered_tasks = {key: value}
                task_list.append(filtered_tasks)
        return task_list

    def run(self, *, module: str, args: list | None = None, kwargs: dict | None = None) -> AsyncResult:
        task = celery_app.send_task(module, args, kwargs)
        return task


TaskService = TaskServiceImpl()
