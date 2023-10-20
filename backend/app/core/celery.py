#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from celery import Celery

from backend.app.core.conf import settings

celery_app = Celery('celery_app')
celery_app.conf.broker_url = f'redis://:{settings.CELERY_REDIS_PASSWORD}@{settings.CELERY_REDIS_HOST}:{settings.CELERY_REDIS_PORT}/{settings.CELERY_REDIS_DATABASE_BROKER}'
celery_app.conf.result_backend = f'redis://:{settings.CELERY_REDIS_PASSWORD}@{settings.CELERY_REDIS_HOST}:{settings.CELERY_REDIS_PORT}/{settings.CELERY_REDIS_DATABASE_BACKEND}'
celery_app.conf.result_backend_transport_options = {
    'global_keyprefix': settings.CELERY_REDIS_BACKEND_PREFIX,
    'retry_policy': {
        'timeout': settings.CELERY_REDIS_BACKEND_TIMEOUT
    },
    'result_chord_ordered': settings.CELERY_REDIS_BACKEND_ORDERED

}
celery_app.conf.timezone = settings.DATETIME_TIMEZONE
celery_app.conf.task_track_started = True
celery_app.autodiscover_tasks(['app'])
