#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from celery.backends.database.models import TaskExtended as TaskResult

OVERWRITE_CELERY_RESULT_TABLE_NAME = 'task_result'
OVERWRITE_CELERY_RESULT_GROUP_TABLE_NAME = 'task_group_result'

# 重写表名配置
TaskResult.configure(name=OVERWRITE_CELERY_RESULT_TABLE_NAME)
