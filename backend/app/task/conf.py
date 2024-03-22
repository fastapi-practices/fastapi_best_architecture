#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from functools import lru_cache
from typing import Literal

from celery.schedules import crontab
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from backend.core.path_conf import BasePath


class TaskSettings(BaseSettings):
    """Task Settings"""

    model_config = SettingsConfigDict(env_file=f'{BasePath}/.env', env_file_encoding='utf-8', extra='ignore')

    # Env Config
    ENVIRONMENT: Literal['dev', 'pro']

    # Env Celery
    CELERY_BROKER_REDIS_DATABASE: int  # 仅当使用 redis 作为 broker 时生效, 更适用于测试环境
    CELERY_BACKEND_REDIS_DATABASE: int

    # Env Rabbitmq
    # docker run -d --hostname fba-mq --name fba-mq  -p 5672:5672 -p 15672:15672 rabbitmq:latest
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_USERNAME: str
    RABBITMQ_PASSWORD: str

    # Celery
    CELERY_BROKER: Literal['rabbitmq', 'redis'] = 'redis'
    CELERY_BACKEND_REDIS_PREFIX: str = 'fba_celery'
    CELERY_BACKEND_REDIS_TIMEOUT: float = 5.0
    CELERY_TASKS_PACKAGES: list[str] = [
        'app.task.celery_task',
        'app.task.celery_task.db_log',
    ]
    CELERY_TASK_MAX_RETRIES: int = 5
    CELERY_SCHEDULE: dict = {
        'exec-every-10-seconds': {
            'task': 'task_demo_async',
            'schedule': 10,
        },
        'exec-every-sunday': {
            'task': 'auto_delete_db_opera_log',
            'schedule': crontab(0, 0, day_of_week='6'),  # type: ignore
        },
        'exec-every-15-of-month': {
            'task': 'auto_delete_db_login_log',
            'schedule': crontab(0, 0, day_of_month='15'),  # type: ignore
        },
    }

    @model_validator(mode='before')
    def validate_celery_broker(cls, values):
        if values['ENVIRONMENT'] == 'pro':
            values['CELERY_BROKER'] = 'rabbitmq'
        return values


@lru_cache
def get_task_settings() -> TaskSettings:
    """获取 task 配置"""
    return TaskSettings()


task_settings = get_task_settings()
