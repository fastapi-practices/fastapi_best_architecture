#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uuid
import sys

sys.path.append('../../')

from backend.app.core.celery import celery_app  # noqa: E402


@celery_app.task
def task_demo_async() -> str:
    uid = uuid.uuid4().hex
    print(f'异步任务 {uid} 执行成功')
    return uid
