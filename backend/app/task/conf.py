#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from functools import lru_cache
from typing import Any, Literal

from celery.schedules import crontab
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from backend.core.path_conf import BASE_PATH


class TaskSettings(BaseSettings):
    """Celery 任务配置"""

    model_config = SettingsConfigDict(env_file=f'{BASE_PATH}/.env', env_file_encoding='utf-8', extra='ignore')

    # .env 环境
    ENVIRONMENT: Literal['dev', 'pro']

    # .env Redis 配置
    CELERY_BROKER_REDIS_DATABASE: int
    CELERY_BACKEND_REDIS_DATABASE: int

    # .env RabbitMQ 配置
    # docker run -d --hostname fba-mq --name fba-mq  -p 5672:5672 -p 15672:15672 rabbitmq:latest
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_USERNAME: str
    RABBITMQ_PASSWORD: str

    # Celery 基础配置
    CELERY_BROKER: Literal['rabbitmq', 'redis'] = 'redis'
    CELERY_BACKEND_REDIS_PREFIX: str = 'fba:celery:'
    CELERY_BACKEND_REDIS_TIMEOUT: int = 5
    CELERY_TASK_PACKAGES: list[str] = [
        'app.task.celery_task',
        'app.task.celery_task.db_log',
    ]
    CELERY_TASK_MAX_RETRIES: int = 5

    # Celery 定时任务配置
    CELERY_SCHEDULE: dict[str, dict[str, Any]] = {
        'exec-every-10-seconds': {
            'task': 'task_demo_async',
            'schedule': 10,
        },
        'exec-every-sunday': {
            'task': 'delete_db_opera_log',
            'schedule': crontab('0', '0', day_of_week='6'),
        },
        'exec-every-15-of-month': {
            'task': 'delete_db_login_log',
            'schedule': crontab('0', '0', day_of_month='15'),
        },
    }

    @model_validator(mode='before')
    @classmethod
    def validate_celery_broker(cls, values: Any) -> Any:
        """生产环境强制使用 RabbitMQ 作为消息代理"""
        if values['ENVIRONMENT'] == 'pro':
            values['CELERY_BROKER'] = 'rabbitmq'
        return values


@lru_cache
def get_task_settings() -> TaskSettings:
    """获取 Celery 任务配置"""
    return TaskSettings()


task_settings = get_task_settings()
