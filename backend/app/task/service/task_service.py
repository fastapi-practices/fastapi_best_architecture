#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from celery.exceptions import NotRegistered
from celery.result import AsyncResult

from backend.app.task.celery import celery_app
from backend.common.exception.errors import NotFoundError


class TaskService:
    @staticmethod
    def get_list():
        filtered_tasks = []
        tasks = celery_app.tasks
        for key, value in tasks.items():
            if not key.startswith('celery.'):
                filtered_tasks.append({key, value})
        return filtered_tasks

    @staticmethod
    def get():
        return celery_app.current_worker_task

    @staticmethod
    def get_status(uid: str):
        try:
            result = AsyncResult(id=uid, app=celery_app)
        except NotRegistered:
            raise NotFoundError(msg='任务不存在')
        return result.status

    @staticmethod
    def get_result(uid: str):
        try:
            result = AsyncResult(id=uid, app=celery_app)
        except NotRegistered:
            raise NotFoundError(msg='任务不存在')
        return result

    @staticmethod
    def run(*, name: str, args: list | None = None, kwargs: dict | None = None):
        task = celery_app.send_task(name=name, args=args, kwargs=kwargs)
        return task


task_service = TaskService()
