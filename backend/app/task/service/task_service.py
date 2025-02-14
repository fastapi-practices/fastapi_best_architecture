#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from celery.exceptions import NotRegistered
from celery.result import AsyncResult
from starlette.concurrency import run_in_threadpool

from backend.app.task.celery import celery_app
from backend.app.task.schema.task import RunParam, TaskResult
from backend.common.exception import errors
from backend.common.exception.errors import NotFoundError


class TaskService:
    @staticmethod
    async def get_list() -> list[str]:
        registered_tasks = await run_in_threadpool(celery_app.control.inspect().registered)
        if not registered_tasks:
            raise errors.ForbiddenError(msg='celery 服务未启动')
        tasks = list(registered_tasks.values())[0]
        return tasks

    @staticmethod
    def get_detail(*, tid: str) -> TaskResult:
        try:
            result = AsyncResult(id=tid, app=celery_app)
        except NotRegistered:
            raise NotFoundError(msg='任务不存在')
        return TaskResult(
            result=result.result,
            traceback=result.traceback,
            status=result.state,
            name=result.name,
            args=result.args,
            kwargs=result.kwargs,
            worker=result.worker,
            retries=result.retries,
            queue=result.queue,
        )

    @staticmethod
    def revoke(*, tid: str):
        try:
            result = AsyncResult(id=tid, app=celery_app)
        except NotRegistered:
            raise NotFoundError(msg='任务不存在')
        result.revoke(terminate=True)

    @staticmethod
    def run(*, obj: RunParam) -> str:
        task: AsyncResult = celery_app.send_task(name=obj.name, args=obj.args, kwargs=obj.kwargs)
        return task.task_id


task_service: TaskService = TaskService()
