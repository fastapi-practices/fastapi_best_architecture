#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from celery import Celery

from backend.app.task.conf import task_settings
from backend.core.conf import settings

__all__ = ['celery_app']


def make_celery(main_name: str) -> Celery:
    """
    创建 celery 应用

    :param main_name: __main__ module name
    :return:
    """
    app = Celery(main_name)
    app.autodiscover_tasks(packages=['backend.app.task'])

    # Celery Config
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html
    _redis_connection = f'redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}'

    # Broker
    app.conf.broker_url = (
        f'{_redis_connection}/{task_settings.CELERY_BROKER_REDIS_DATABASE}'
        if task_settings.CELERY_BROKER == 'redis'
        else f'amqp://{task_settings.RABBITMQ_USERNAME}:{task_settings.RABBITMQ_PASSWORD}@{task_settings.RABBITMQ_HOST}:{task_settings.RABBITMQ_PORT}'
    )

    # Result Backend
    app.conf.result_backend = f'{_redis_connection}/{task_settings.CELERY_BACKEND_REDIS_DATABASE}'
    app.conf.result_backend_transport_options = {
        'global_keyprefix': task_settings.CELERY_BACKEND_REDIS_PREFIX,
        'retry_policy': {
            'timeout': task_settings.CELERY_BACKEND_REDIS_TIMEOUT,
        },
        'result_chord_ordered': task_settings.CELERY_BACKEND_REDIS_ORDERED,
    }

    # Extra Conf
    app.conf.timezone = settings.DATETIME_TIMEZONE
    app.conf.task_track_started = True

    # Celery Schedule Tasks
    # https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html
    app.conf.beat_schedule = task_settings.CELERY_BEAT_SCHEDULE
    app.conf.beat_schedule_filename = task_settings.CELERY_BEAT_SCHEDULE_FILENAME

    return app


celery_app = make_celery('celery_app')
