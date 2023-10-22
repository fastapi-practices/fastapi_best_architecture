#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uuid
import sys

sys.path.append('../../')

from backend.app.core.celery import celery_app  # noqa: E402


@celery_app.task
def task_demo_async():
    print(f'异步任务 {uuid.uuid4().hex}')
