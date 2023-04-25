#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime

from fastapi import APIRouter, Query
from typing_extensions import Annotated

from backend.app.common.task import scheduler

router = APIRouter()


def task_demo():
    print('普通任务')


async def task_demo_async():
    print('异步任务')


@router.get('', summary='获取任务')
async def task_demo_get():
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


@router.post('', summary='添加同步任务')
async def task_demo_add():
    scheduler.add_job(
        task_demo, 'interval', seconds=1, id='task_demo', replace_existing=True, start_date=datetime.datetime.now()
    )

    return {'msg': 'success'}


@router.post('/async', summary='添加异步任务')
async def task_demo_add_async():
    scheduler.add_job(
        task_demo_async,
        'interval',
        seconds=1,
        id='task_demo_async',
        replace_existing=True,
        start_date=datetime.datetime.now(),
    )

    return {'msg': 'success'}


@router.delete('', summary='删除任务')
async def task_demo_delete(job_id: Annotated[str, Query(..., description='任务id')]):
    scheduler.remove_job(job_id=job_id)

    return {'msg': 'success'}
