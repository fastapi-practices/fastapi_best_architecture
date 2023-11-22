#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from celery.exceptions import BackendGetMetaError, NotRegistered
from celery.result import AsyncResult

from backend.app.common.celery import celery_app
from backend.app.common.exception.errors import NotFoundError


class TaskService:
    @staticmethod
    def get(pk: str) -> AsyncResult | None:
        try:
            result = celery_app.AsyncResult(pk)
        except (BackendGetMetaError, NotRegistered):
            raise NotFoundError(msg='任务不存在')
        if result.failed():
            return None
        return result

    @staticmethod
    def gets() -> dict:
        filtered_tasks = {}
        tasks = celery_app.tasks
        for key, value in tasks.items():
            if not key.startswith('celery.'):
                filtered_tasks[key] = value
        return filtered_tasks

    @staticmethod
    def run(*, module: str, args: list | None = None, kwargs: dict | None = None) -> AsyncResult:
        task = celery_app.send_task(module, args, kwargs)
        return task
