#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uuid

from backend.app.core.celery import celery_app


@celery_app.task()
async def task_demo_async():
    print(f'异步任务 {uuid.uuid4().hex}')
