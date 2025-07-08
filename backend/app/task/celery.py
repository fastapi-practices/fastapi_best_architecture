#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import celery
import celery_aio_pool

from backend.app.task.tasks.beat import LOCAL_BEAT_SCHEDULE
from backend.core.conf import settings


def init_celery() -> celery.Celery:
    """初始化 Celery 应用"""

    # TODO: Update this work if celery version >= 6.0.0
    # https://github.com/fastapi-practices/fastapi_best_architecture/issues/321
    # https://github.com/celery/celery/issues/7874
    celery.app.trace.build_tracer = celery_aio_pool.build_async_tracer
    celery.app.trace.reset_worker_optimizations()

    app = celery.Celery(
        'fba_celery',
        enable_utc=False,
        timezone=settings.DATETIME_TIMEZONE,
        beat_schedule=LOCAL_BEAT_SCHEDULE,
        broker_url=(
            f'redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:'
            f'{settings.REDIS_PORT}/{settings.CELERY_BROKER_REDIS_DATABASE}'
        )
        if settings.CELERY_BROKER == 'redis'
        else (
            f'amqp://{settings.CELERY_RABBITMQ_USERNAME}:{settings.CELERY_RABBITMQ_PASSWORD}@'
            f'{settings.CELERY_RABBITMQ_HOST}:{settings.CELERY_RABBITMQ_PORT}'
        ),
        broker_connection_retry_on_startup=True,
        result_backend=(
            f'redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:'
            f'{settings.REDIS_PORT}/{settings.CELERY_BACKEND_REDIS_DATABASE}'
        ),
        result_backend_transport_options={
            'global_keyprefix': settings.CELERY_BACKEND_REDIS_PREFIX,
            'retry_policy': {
                'timeout': settings.CELERY_BACKEND_REDIS_TIMEOUT,
            },
        },
        task_cls='app.task.tasks.base:TaskBase',
        task_track_started=True,
    )

    # 自动发现任务
    app.autodiscover_tasks(settings.CELERY_TASK_PACKAGES)

    return app


# 创建 Celery 实例
celery_app: celery.Celery = init_celery()
