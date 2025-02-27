#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import celery
import celery_aio_pool

from backend.app.task.conf import task_settings
from backend.core.conf import settings

__all__ = ['celery_app']


def init_celery() -> celery.Celery:
    """初始化 celery 应用"""

    # TODO: Update this work if celery version >= 6.0.0
    # https://github.com/fastapi-practices/fastapi_best_architecture/issues/321
    # https://github.com/celery/celery/issues/7874
    celery.app.trace.build_tracer = celery_aio_pool.build_async_tracer
    celery.app.trace.reset_worker_optimizations()

    # Celery Schedule Tasks
    # https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html
    beat_schedule = task_settings.CELERY_SCHEDULE

    # Celery Config
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html
    broker_url = (
        (
            f'redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:'
            f'{settings.REDIS_PORT}/{task_settings.CELERY_BROKER_REDIS_DATABASE}'
        )
        if task_settings.CELERY_BROKER == 'redis'
        else (
            f'amqp://{task_settings.RABBITMQ_USERNAME}:{task_settings.RABBITMQ_PASSWORD}@'
            f'{task_settings.RABBITMQ_HOST}:{task_settings.RABBITMQ_PORT}'
        )
    )
    result_backend = (
        f'redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:'
        f'{settings.REDIS_PORT}/{task_settings.CELERY_BACKEND_REDIS_DATABASE}'
    )
    result_backend_transport_options = {
        'global_keyprefix': f'{task_settings.CELERY_BACKEND_REDIS_PREFIX}',
        'retry_policy': {
            'timeout': task_settings.CELERY_BACKEND_REDIS_TIMEOUT,
        },
    }

    app = celery.Celery(
        'fba_celery',
        enable_utc=False,
        timezone=settings.DATETIME_TIMEZONE,
        beat_schedule=beat_schedule,
        broker_url=broker_url,
        broker_connection_retry_on_startup=True,
        result_backend=result_backend,
        result_backend_transport_options=result_backend_transport_options,
        task_cls='app.task.celery_task.base:TaskBase',
        task_track_started=True,
    )

    # Load task modules
    app.autodiscover_tasks(task_settings.CELERY_TASK_PACKAGES)

    return app


# 创建 celery 实例
celery_app: celery.Celery = init_celery()
