#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from celery import Celery

from backend.app.task.conf import task_settings
from backend.core.conf import settings

__all__ = ['celery_app']


def init_celery() -> Celery:
    """创建 celery 应用"""
    app = Celery('fba_app')
    app.autodiscover_tasks(packages=['tasks'])

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
    # TODO
    _result_backend_transport_options = {
        'global_keyprefix': task_settings.CELERY_BACKEND_REDIS_PREFIX,
        'retry_policy': {
            'timeout': task_settings.CELERY_BACKEND_REDIS_TIMEOUT,
        },
        'result_chord_ordered': task_settings.CELERY_BACKEND_REDIS_ORDERED,
    }
    app.conf.broker_url = _redis_broker if task_settings.CELERY_BROKER == 'redis' else _amqp_broker
    app.conf.result_backend = _result_backend
    app.conf.result_backend_transport_options = _result_backend_transport_options
    app.conf.timezone = settings.DATETIME_TIMEZONE
    app.conf.enable_utc = False
    app.conf.task_track_started = True

    # Celery Schedule Tasks
    # https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html
    app.conf.beat_schedule = task_settings.CELERY_BEAT_SCHEDULE
    app.conf.beat_schedule_filename = task_settings.CELERY_BEAT_SCHEDULE_FILENAME

    return app


celery_app = init_celery()
