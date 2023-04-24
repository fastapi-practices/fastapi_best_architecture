# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import tzlocal
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from backend.app.common.log import log
from backend.app.core.conf import settings


def _scheduler_conf() -> dict:
    """
    task conf

    :return:
    """
    redis_conf = {
        'host': settings.APS_REDIS_HOST,
        'port': settings.APS_REDIS_PORT,
        'password': settings.APS_REDIS_PASSWORD,
        'db': settings.APS_REDIS_DATABASE,
        'socket_timeout': settings.APS_REDIS_TIMEOUT,
    }

    end_conf = {
        # 配置存储器
        "jobstores": {'default': RedisJobStore(**redis_conf)},
        # 配置执行器
        "executors": {
            'default': AsyncIOExecutor(),
        },
        # 创建task时的默认参数
        "job_defaults": {
            'coalesce': settings.APS_COALESCE,
            'max_instances': settings.APS_MAX_INSTANCES,
            "misfire_grace_time": settings.APS_MISFIRE_GRACE_TIME,
        },
        # 时区
        "timezone": str(tzlocal.get_localzone()),
    }

    return end_conf


class Scheduler(AsyncIOScheduler):
    def start(self, paused: bool = False):
        try:
            super().start(paused)
        except Exception as e:
            log.error(f'❌ 任务 scheduler 启动失败: {e}')

    def shutdown(self, wait: bool = True):
        try:
            super().shutdown(wait)
        except Exception as e:
            log.error(f'❌ 任务 scheduler 关闭失败: {e}')


# 调度器
scheduler = Scheduler(**_scheduler_conf())
