#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from celery.schedules import schedule

from backend.app.task.utils.tzcrontab import TzAwareCrontab

LOCAL_BEAT_SCHEDULE = {
    'exec_every_10_seconds': {
        'task': 'task_demo_async',
        'schedule': schedule(10),
    },
    'exec_every_1_minute_of_hour': {
        'task': 'task_demo_async',
        'schedule': TzAwareCrontab('1'),
    },
    'exec_every_sunday': {
        'task': 'delete_db_opera_log',
        'schedule': TzAwareCrontab('0', '0', day_of_week='6'),
    },
    'exec_every_15_of_month': {
        'task': 'delete_db_login_log',
        'schedule': TzAwareCrontab('0', '0', day_of_month='15'),
    },
}
