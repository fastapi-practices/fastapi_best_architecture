#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uuid

from anyio import sleep

from backend.app.task.celery import celery_app


@celery_app.task(name='task_demo_async')
async def task_demo_async() -> str:
    await sleep(1)
    uid = uuid.uuid4().hex
    print(f'异步任务 {uid} 执行成功')
    return uid
