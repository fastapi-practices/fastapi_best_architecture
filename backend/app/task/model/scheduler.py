#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio

from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    String,
    event,
)
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.dialects.postgresql import INTEGER, TEXT
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.exception import errors
from backend.common.model import Base, TimeZone, id_key
from backend.core.conf import settings
from backend.database.redis import redis_client
from backend.utils.timezone import timezone


class TaskScheduler(Base):
    """任务调度表"""

    __tablename__ = 'task_scheduler'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(50), unique=True, comment='任务名称')
    task: Mapped[str] = mapped_column(String(255), comment='要运行的 Celery 任务')
    args: Mapped[str | None] = mapped_column(JSON(), comment='任务可接收的位置参数')
    kwargs: Mapped[str | None] = mapped_column(JSON(), comment='任务可接收的关键字参数')
    queue: Mapped[str | None] = mapped_column(String(255), comment='CELERY_TASK_QUEUES 中定义的队列')
    exchange: Mapped[str | None] = mapped_column(String(255), comment='低级别 AMQP 路由的交换机')
    routing_key: Mapped[str | None] = mapped_column(String(255), comment='低级别 AMQP 路由的路由密钥')
    start_time: Mapped[datetime | None] = mapped_column(TimeZone, comment='任务开始触发的时间')
    expire_time: Mapped[datetime | None] = mapped_column(TimeZone, comment='任务不再触发的截止时间')
    expire_seconds: Mapped[int | None] = mapped_column(comment='任务不再触发的秒数时间差')
    type: Mapped[int] = mapped_column(comment='调度类型（0间隔 1定时）')
    interval_every: Mapped[int | None] = mapped_column(comment='任务再次运行前的间隔周期数')
    interval_period: Mapped[str | None] = mapped_column(String(255), comment='任务运行之间的周期类型')
    crontab: Mapped[str | None] = mapped_column(String(50), default='* * * * *', comment='任务运行的 Crontab 计划')
    one_off: Mapped[bool] = mapped_column(
        Boolean().with_variant(INTEGER, 'postgresql'), default=False, comment='是否仅运行一次'
    )
    enabled: Mapped[bool] = mapped_column(
        Boolean().with_variant(INTEGER, 'postgresql'), default=True, comment='是否启用任务'
    )
    total_run_count: Mapped[int] = mapped_column(default=0, comment='任务触发的总次数')
    last_run_time: Mapped[datetime | None] = mapped_column(TimeZone, default=None, comment='任务最后触发的时间')
    remark: Mapped[str | None] = mapped_column(
        LONGTEXT().with_variant(TEXT, 'postgresql'), default=None, comment='备注'
    )

    no_changes: bool = False

    @staticmethod
    def before_insert_or_update(mapper, connection, target):
        if target.expire_seconds is not None and target.expire_time:
            raise errors.ConflictError(msg='expires 和 expire_seconds 只能设置一个')

    @classmethod
    def changed(cls, mapper, connection, target):
        if not target.no_changes:
            cls.update_changed(mapper, connection, target)

    @classmethod
    async def update_changed_async(cls):
        now = timezone.now()
        await redis_client.set(f'{settings.CELERY_REDIS_PREFIX}:last_update', timezone.to_str(now))

    @classmethod
    def update_changed(cls, mapper, connection, target):
        asyncio.create_task(cls.update_changed_async())


# 事件监听器
event.listen(TaskScheduler, 'before_insert', TaskScheduler.before_insert_or_update)
event.listen(TaskScheduler, 'before_update', TaskScheduler.before_insert_or_update)
event.listen(TaskScheduler, 'after_insert', TaskScheduler.update_changed)
event.listen(TaskScheduler, 'after_delete', TaskScheduler.update_changed)
event.listen(TaskScheduler, 'after_update', TaskScheduler.changed)
