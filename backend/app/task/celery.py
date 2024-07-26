#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import celery
import celery_aio_pool

from backend.app.task.conf import task_settings
from backend.core.conf import settings

__all__ = ['celery_app']


def init_celery() -> celery.Celery:
    """创建 celery 应用"""

    # TODO: Update this work if celery version >= 6.0.0
    # https://github.com/fastapi-practices/fastapi_best_architecture/issues/321
    # https://github.com/celery/celery/issues/7874
    celery.app.trace.build_tracer = celery_aio_pool.build_async_tracer
    celery.app.trace.reset_worker_optimizations()

    app = celery.Celery(
        'fba_celery',
        broker_connection_retry_on_startup=True,
        worker_pool=celery_aio_pool.pool.AsyncIOPool,
        trace=celery_aio_pool.build_async_tracer,
    )

    # Celery Config
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html
    _redis_broker = (
        f'redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:'
        f'{settings.REDIS_PORT}/{task_settings.CELERY_BROKER_REDIS_DATABASE}'
    )
    _amqp_broker = (
        f'amqp://{task_settings.RABBITMQ_USERNAME}:{task_settings.RABBITMQ_PASSWORD}@'
        f'{task_settings.RABBITMQ_HOST}:{task_settings.RABBITMQ_PORT}'
    )
    _result_backend = (
        f'redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:'
        f'{settings.REDIS_PORT}/{task_settings.CELERY_BACKEND_REDIS_DATABASE}'
    )
    _result_backend_transport_options = {
        'global_keyprefix': f'{task_settings.CELERY_BACKEND_REDIS_PREFIX}_',
        'retry_policy': {
            'timeout': task_settings.CELERY_BACKEND_REDIS_TIMEOUT,
        },
    }

    # Celery Schedule Tasks
    # https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html
    _beat_schedule = task_settings.CELERY_SCHEDULE

    # Update celery settings
    app.conf.update(
        broker_url=_redis_broker if task_settings.CELERY_BROKER == 'redis' else _amqp_broker,
        result_backend=_result_backend,
        result_backend_transport_options=_result_backend_transport_options,
        timezone=settings.DATETIME_TIMEZONE,
        enable_utc=False,
        task_track_started=True,
        beat_schedule=_beat_schedule,
    )

    # Load task modules
    app.autodiscover_tasks(task_settings.CELERY_TASKS_PACKAGES)

    return app


# 创建 celery 实例
celery_app = init_celery()
