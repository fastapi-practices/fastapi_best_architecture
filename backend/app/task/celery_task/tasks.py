#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from anyio import sleep

from backend.app.task.celery import celery_app


@celery_app.task(name='task_demo_async')
async def task_demo_async() -> str:
    """异步示例任务，模拟耗时操作"""
    await sleep(20)
    return 'test async'
