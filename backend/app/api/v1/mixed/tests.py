#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime

from fastapi import APIRouter, File, UploadFile, Form

from backend.app.common.response.response_schema import response_base
from backend.app.common.task import scheduler

router = APIRouter(prefix='/tests')


def task_demo():
    print('普通任务')


async def task_demo_async():
    print('异步任务')


@router.post('/sync', summary='测试添加同步任务')
async def task_demo_add():
    scheduler.add_job(
        task_demo, 'interval', seconds=1, id='task_demo', replace_existing=True, start_date=datetime.datetime.now()
    )

    return await response_base.success({'msg': 'success'})


@router.post('/async', summary='测试添加异步任务')
async def task_demo_add_async():
    scheduler.add_job(
        task_demo_async,
        'interval',
        seconds=1,
        id='task_demo_async',
        replace_existing=True,
        start_date=datetime.datetime.now(),
    )
    return await response_base.success({'msg': 'success'})


@router.post('/files', summary='测试文件上传')
async def create_file(file: bytes = File(), fileb: UploadFile = File(), token: str = Form()):
    return {
        'file_size': len(file),
        'token': token,
        'fileb_content_type': fileb.content_type,
    }
