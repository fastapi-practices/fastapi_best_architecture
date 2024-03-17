#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import uuid

sys.path.append('../../../')

from backend.app.task.celery import celery_app


@celery_app.task
def task_demo_async() -> str:
    uid = uuid.uuid4().hex
    print(f'异步任务 {uid} 执行成功')
    return uid
