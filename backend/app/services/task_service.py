#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from asgiref.sync import sync_to_async

from backend.app.common.exception import errors
from backend.app.common.task import scheduler
from backend.app.utils.timezone import timezone_utils


class TaskService:
    @staticmethod
    @sync_to_async
    def get_task_list():
        tasks = []
        for job in scheduler.get_jobs():
            tasks.append(
                {
                    'id': job.id,
                    'func_name': job.func_ref,
                    'trigger': str(job.trigger),
                    'executor': job.executor,
                    'name': job.name,
                    'misfire_grace_time': job.misfire_grace_time,
                    'coalesce': job.coalesce,
                    'max_instances': job.max_instances,
                    'next_run_time': job.next_run_time,
                }
            )
        return tasks

    @staticmethod
    @sync_to_async
    def get_task(pk: str):
        job = scheduler.get_job(job_id=pk)
        if not job:
            raise errors.NotFoundError(msg='任务不存在')
        task = {
            'id': job.id,
            'func_name': job.func_ref,
            'trigger': str(job.trigger),
            'executor': job.executor,
            'name': job.name,
            'misfire_grace_time': job.misfire_grace_time,
            'coalesce': job.coalesce,
            'max_instances': job.max_instances,
            'next_run_time': job.next_run_time,
        }

        return task

    async def run(self, pk: str):
        task = await self.get_task(pk=pk)
        scheduler.modify_job(job_id=pk, next_run_time=timezone_utils.get_timezone_datetime())
        return task

    async def pause(self, pk: str):
        task = await self.get_task(pk=pk)
        scheduler.pause_job(job_id=pk)
        return task

    async def resume(self, pk: str):
        task = await self.get_task(pk=pk)
        scheduler.resume_job(job_id=pk)
        return task

    async def delete(self, pk: str):
        task = await self.get_task(pk=pk)
        scheduler.remove_job(job_id=pk)
        return task
