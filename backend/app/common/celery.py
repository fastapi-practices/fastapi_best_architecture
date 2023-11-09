#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from celery import Celery

from backend.app.core.conf import settings

__all__ = ['celery_app']


def make_celery(main_name: str) -> Celery:
    """
    创建 celery 应用

    :param main_name: __main__ module name
    :return:
    """
    app = Celery(main_name)
    app.autodiscover_tasks(packages=['backend.app'])

    # Celery Config
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html
    app.conf.broker_url = (
        (
            f'redis://:{settings.CELERY_REDIS_PASSWORD}@{settings.CELERY_REDIS_HOST}:'
            f'{settings.CELERY_REDIS_PORT}/{settings.CELERY_BROKER_REDIS_DATABASE}'
        )
        if settings.CELERY_BROKER == 'redis'
        else (
            f'amqp://{settings.RABBITMQ_USERNAME}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}:'
            f'{settings.RABBITMQ_PORT}'
        )
    )
    app.conf.result_backend = (
        f'redis://:{settings.CELERY_REDIS_PASSWORD}@{settings.CELERY_REDIS_HOST}:'
        f'{settings.CELERY_REDIS_PORT}/{settings.CELERY_BACKEND_REDIS_DATABASE}'
    )
    app.conf.result_backend_transport_options = {
        'global_keyprefix': settings.CELERY_BACKEND_REDIS_PREFIX,
        'retry_policy': {
            'timeout': settings.CELERY_BACKEND_REDIS_TIMEOUT,
        },
        'result_chord_ordered': settings.CELERY_BACKEND_REDIS_ORDERED,
    }
    app.conf.timezone = settings.DATETIME_TIMEZONE
    app.conf.task_track_started = True

    # Celery Schedule Tasks
    # https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html
    app.conf.beat_schedule = settings.CELERY_BEAT_SCHEDULE
    app.conf.beat_schedule_filename = settings.CELERY_BEAT_SCHEDULE_FILENAME

    return app


celery_app = make_celery('celery_app')
