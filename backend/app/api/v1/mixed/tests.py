#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.common.response.response_schema import response_base
from backend.app.tasks import task_demo_async

router = APIRouter(prefix='/tests')


@router.post('/send', summary='测试异步任务')
async def task_send():
    result = task_demo_async.delay()
    return await response_base.success(data=result.id)


@router.post('/send', summary='异步任务演示')
async def send_task():
    result = task_demo_async.delay()
    return await response_base.success(data=result.id)
