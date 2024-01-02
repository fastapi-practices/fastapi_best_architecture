#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, File, Form, UploadFile

from backend.app.common.response.response_schema import response_base
from backend.app.tasks import task_demo_async

router = APIRouter(prefix='/tests')


@router.post('/send', summary='异步任务演示')
async def send_task():
    result = task_demo_async.delay()
    return await response_base.success(data=result.id)


@router.post('/files', summary='上传文件演示')
async def create_file(
    file: Annotated[bytes, File()],
    fileb: Annotated[UploadFile, File()],
    token: Annotated[str, Form()],
):
    return {
        'file_size': len(file),
        'token': token,
        'fileb_content_type': fileb.content_type,
    }
