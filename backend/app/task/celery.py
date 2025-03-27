#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any

import celery
import celery_aio_pool

from backend.app.task.conf import task_settings
from backend.core.conf import settings

__all__ = ['celery_app']


def get_broker_url() -> str:
    """获取消息代理 URL"""
    if task_settings.CELERY_BROKER == 'redis':
        return (
            f'redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:'
            f'{settings.REDIS_PORT}/{task_settings.CELERY_BROKER_REDIS_DATABASE}'
        )
    return (
        f'amqp://{task_settings.RABBITMQ_USERNAME}:{task_settings.RABBITMQ_PASSWORD}@'
        f'{task_settings.RABBITMQ_HOST}:{task_settings.RABBITMQ_PORT}'
    )


def get_result_backend() -> str:
    """获取结果后端 URL"""
    return (
        f'redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:'
        f'{settings.REDIS_PORT}/{task_settings.CELERY_BACKEND_REDIS_DATABASE}'
    )


def get_result_backend_transport_options() -> dict[str, Any]:
    """获取结果后端传输选项"""
    return {
        'global_keyprefix': task_settings.CELERY_BACKEND_REDIS_PREFIX,
        'retry_policy': {
            'timeout': task_settings.CELERY_BACKEND_REDIS_TIMEOUT,
        },
    }


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
        beat_schedule=task_settings.CELERY_SCHEDULE,
        broker_url=get_broker_url(),
        broker_connection_retry_on_startup=True,
        result_backend=get_result_backend(),
        result_backend_transport_options=get_result_backend_transport_options(),
        task_cls='app.task.celery_task.base:TaskBase',
        task_track_started=True,
    )

    # 自动发现任务
    app.autodiscover_tasks(task_settings.CELERY_TASK_PACKAGES)

    return app


# 创建 Celery 实例
celery_app: celery.Celery = init_celery()
