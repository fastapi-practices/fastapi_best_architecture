#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, File, Form, UploadFile

from backend.app.tasks import task_demo_async

router = APIRouter(prefix='/tests')


@router.post('/send', summary='测试异步任务')
async def task_send():
    result = task_demo_async.delay()
    return {'msg': 'Success', 'data': result.id}


@router.post('/files', summary='测试文件上传')
async def create_file(file: bytes = File(), fileb: UploadFile = File(), token: str = Form()):
    return {
        'file_size': len(file),
        'token': token,
        'fileb_content_type': fileb.content_type,
    }
