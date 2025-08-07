#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import celery
import celery_aio_pool

from backend.app.task.model.result import OVERWRITE_CELERY_RESULT_GROUP_TABLE_NAME, OVERWRITE_CELERY_RESULT_TABLE_NAME
from backend.app.task.tasks.beat import LOCAL_BEAT_SCHEDULE
from backend.core.conf import settings
from backend.core.path_conf import BASE_PATH


def find_task_packages():
    packages = []
    task_dir = os.path.join(BASE_PATH, 'app', 'task', 'tasks')
    for root, dirs, files in os.walk(task_dir):
        if 'tasks.py' in files:
            package = root.replace(str(BASE_PATH.parent) + os.path.sep, '').replace(os.path.sep, '.')
            packages.append(package)
    return packages


def init_celery() -> celery.Celery:
    """初始化 Celery 应用"""

    # TODO: Update this work if celery version >= 6.0.0
    # https://github.com/fastapi-practices/fastapi_best_architecture/issues/321
    # https://github.com/celery/celery/issues/7874
    celery.app.trace.build_tracer = celery_aio_pool.build_async_tracer
    celery.app.trace.reset_worker_optimizations()

    app = celery.Celery(
        'fba_celery',
        broker=f'redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.CELERY_BROKER_REDIS_DATABASE}'
        if settings.CELERY_BROKER == 'redis'
        else f'amqp://{settings.CELERY_RABBITMQ_USERNAME}:{settings.CELERY_RABBITMQ_PASSWORD}@{settings.CELERY_RABBITMQ_HOST}:{settings.CELERY_RABBITMQ_PORT}',
        broker_connection_retry_on_startup=True,
        backend=f'db+{settings.DATABASE_TYPE}+{"pymysql" if settings.DATABASE_TYPE == "mysql" else "psycopg"}'
        f'://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_SCHEMA}',
        database_engine_options={'echo': settings.DATABASE_ECHO},
        database_table_names={
            'task': OVERWRITE_CELERY_RESULT_TABLE_NAME,
            'group': OVERWRITE_CELERY_RESULT_GROUP_TABLE_NAME,
        },
        result_extended=True,
        # result_expires=0,  # 清理任务结果，默认每天凌晨 4 点，0 或 None 表示不清理
        # beat_sync_every=1,  # 保存任务状态周期，默认 3 * 60 秒
        beat_schedule=LOCAL_BEAT_SCHEDULE,
        beat_scheduler='backend.app.task.utils.schedulers:DatabaseScheduler',
        task_cls='backend.app.task.tasks.base:TaskBase',
        task_track_started=True,
        enable_utc=False,
        timezone=settings.DATETIME_TIMEZONE,
    )

    # 自动发现任务
    packages = find_task_packages()
    app.autodiscover_tasks(packages)

    return app


# 创建 Celery 实例
celery_app: celery.Celery = init_celery()
