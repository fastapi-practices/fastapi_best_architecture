#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import APIRouter, File, UploadFile, Form

from backend.app.core.celery import celery_app

router = APIRouter(prefix='/tests')


@router.post('/task/async', summary='测试异步任务')
async def task_demo_async_send():
    celery_app.send_task('task_demo_async')
    return {'msg': 'Success'}


@router.post('/files', summary='测试文件上传')
async def create_file(file: bytes = File(), fileb: UploadFile = File(), token: str = Form()):
    return {
        'file_size': len(file),
        'token': token,
        'fileb_content_type': fileb.content_type,
    }
