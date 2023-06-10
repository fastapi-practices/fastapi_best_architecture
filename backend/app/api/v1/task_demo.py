#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime

from fastapi import Query
from typing_extensions import Annotated

from backend.app.common.task import scheduler


def task_demo():
    print('普通任务')


async def task_demo_async():
    print('异步任务')


async def get_all_task_demos():
    """获取所有任务示例"""
    tasks = []
    for job in scheduler.get_jobs():
        tasks.append(
            {
                'id': job.id,
                'func_name': job.func_ref,
                'trigger': str(job.trigger),
                'executor': job.executor,
                # "args": str(job.args),
                # "kwargs": job.kwargs,
                'name': job.name,
                'misfire_grace_time': job.misfire_grace_time,
                'coalesce': job.coalesce,
                'max_instances': job.max_instances,
                'next_run_time': job.next_run_time,
            }
        )
    return {'msg': 'success', 'data': tasks}


async def create_sync_task_demo():
    """创建同步任务示例"""
    scheduler.add_job(
        task_demo, 'interval', seconds=1, id='task_demo', replace_existing=True, start_date=datetime.datetime.now()
    )

    return {'msg': 'success'}


async def create_async_task_demo():
    """创建异步任务示例"""
    scheduler.add_job(
        task_demo_async,
        'interval',
        seconds=1,
        id='task_demo_async',
        replace_existing=True,
        start_date=datetime.datetime.now(),
    )

    return {'msg': 'success'}


async def delete_task_demo(job_id: Annotated[str, Query(..., description='任务id')]):
    """删除任务示例"""
    scheduler.remove_job(job_id=job_id)

    return {'msg': 'success'}
