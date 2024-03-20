#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from functools import lru_cache
from typing import Literal

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class TaskSettings(BaseSettings):
    """Task Settings"""

    model_config = SettingsConfigDict(env_file='../../.env', env_file_encoding='utf-8', extra='allow')

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
    CELERY_BACKEND_REDIS_ORDERED: bool = True
    CELERY_BEAT_SCHEDULE_FILENAME: str = './log/celery_beat-schedule'
    CELERY_BEAT_SCHEDULE: dict = {
        'task_demo_async': {
            'task': 'tasks.task_demo_async',
            'schedule': 5.0,
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
