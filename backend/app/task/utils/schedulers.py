#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import json
import math

from datetime import datetime, timedelta
from multiprocessing.util import Finalize

from celery import current_app, schedules
from celery.beat import ScheduleEntry, Scheduler
from celery.utils.log import get_logger
from sqlalchemy import select
from sqlalchemy.exc import DatabaseError, InterfaceError

from backend.app.task.enums import PeriodType, TaskSchedulerType
from backend.app.task.model.scheduler import TaskScheduler
from backend.app.task.schema.scheduler import CreateTaskSchedulerParam
from backend.app.task.utils.tzcrontab import TzAwareCrontab, crontab_verify
from backend.common.exception import errors
from backend.core.conf import settings
from backend.database.db import async_db_session
from backend.database.redis import redis_client
from backend.utils._await import run_await
from backend.utils.serializers import select_as_dict
from backend.utils.timezone import timezone

# 此计划程序必须比常规的 5 分钟更频繁地唤醒，因为它需要考虑对计划的外部更改
DEFAULT_MAX_INTERVAL = 5  # seconds

logger = get_logger('fba.schedulers')


class ModelEntry(ScheduleEntry):
    """任务调度实体"""

    def __init__(self, model: TaskScheduler, app=None):
        super().__init__(
            app=app or current_app._get_current_object(),
            name=model.name,
            task=model.task,
        )
        try:
            if (
                model.type == TaskSchedulerType.INTERVAL
                and model.interval_every is not None
                and model.interval_period is not None
            ):
                self.schedule = schedules.schedule(timedelta(**{model.interval_period: model.interval_every}))
            elif model.type == TaskSchedulerType.CRONTAB and model.crontab_minute is not None:
                self.schedule = TzAwareCrontab(
                    minute=model.crontab_minute,
                    hour=model.crontab_hour or '*',
                    day_of_week=model.crontab_day_of_week or '*',
                    day_of_month=model.crontab_day_of_month or '*',
                    month_of_year=model.crontab_month_of_year or '*',
                )
            else:
                raise errors.NotFoundError(msg=f'{self.name} 计划为空！')
            # logger.debug('Schedule: {}'.format(self.schedule))
        except Exception as e:
            logger.error(f'禁用计划为空的任务 {self.name}，详情：{e}')
            asyncio.create_task(self._disable(model))

        try:
            self.args = json.loads(model.args) if model.args else []
            self.kwargs = json.loads(model.kwargs) if model.kwargs else {}
        except ValueError as exc:
            logger.error(f'禁用参数错误的任务：{self.name}；error: {str(exc)}')
            asyncio.create_task(self._disable(model))

        self.options = {}
        for option in ['queue', 'exchange', 'routing_key']:
            value = getattr(model, option)
            if value is None:
                continue
            self.options[option] = value

        expires = getattr(model, 'expires_', None)
        if expires:
            if isinstance(expires, int):
                self.options['expires'] = expires
            elif isinstance(expires, datetime):
                self.options['expires'] = timezone.from_datetime(expires)

        if not model.last_run_time:
            model.last_run_time = timezone.now()
            if model.start_time:
                model.last_run_time = timezone.from_datetime(model.start_time) - timedelta(days=365)

        self.last_run_at = timezone.from_datetime(model.last_run_time)
        self.options['periodic_task_name'] = model.name
        self.model = model

    async def _disable(self, model: TaskScheduler) -> None:
        """禁用任务"""
        model.no_changes = True
        self.model.enabled = self.enabled = model.enabled = False
        async with async_db_session.begin():
            setattr(model, 'enabled', False)

    def is_due(self) -> tuple[bool, int | float]:
        """任务到期状态"""
        if not self.model.enabled:
            # 重新启用时延迟 5 秒
            return schedules.schedstate(is_due=False, next=5)

        # 仅在 'start_time' 之后运行
        if self.model.start_time is not None:
            now = timezone.now()
            start_time = timezone.from_datetime(self.model.start_time)
            if now < start_time:
                delay = math.ceil((start_time - now).total_seconds())
                return schedules.schedstate(is_due=False, next=delay)

        # 一次性任务
        if self.model.one_off and self.model.enabled and self.model.total_run_count > 0:
            self.model.enabled = False
            self.model.total_run_count = 0
            self.model.no_changes = False
            save_fields = ('enabled',)
            run_await(self.save)(save_fields)
            return schedules.schedstate(is_due=False, next=1000000000)  # 高延迟，避免重新检查

        return self.schedule.is_due(self.last_run_at)

    def __next__(self):
        self.model.last_run_time = timezone.now()
        self.model.total_run_count += 1
        self.model.no_changes = True
        return self.__class__(self.model)

    next = __next__

    async def save(self, fields: tuple = ()):
        """
        保存任务状态字段

        :param fields: 要保存的其他字段
        :return:
        """
        async with async_db_session.begin() as db:
            stmt = select(TaskScheduler).where(TaskScheduler.id == self.model.id).with_for_update()
            query = await db.execute(stmt)
            task = query.scalars().first()
            if task:
                for field in ['last_run_time', 'total_run_count', 'no_changes']:
                    setattr(task, field, getattr(self.model, field))
                for field in fields:
                    setattr(task, field, getattr(self.model, field))
            else:
                logger.warning(f'任务 {self.model.name} 不存在，跳过更新')

    @classmethod
    async def from_entry(cls, name, app=None, **entry):
        """保存或更新本地任务调度"""
        async with async_db_session.begin() as db:
            stmt = select(TaskScheduler).where(TaskScheduler.name == name)
            query = await db.execute(stmt)
            task = query.scalars().first()
            temp = await cls._unpack_fields(name, **entry)
            if not task:
                task = TaskScheduler(**temp)
                db.add(task)
            else:
                for key, value in temp.items():
                    setattr(task, key, value)
            res = cls(task, app=app)
            return res

    @staticmethod
    async def to_model_schedule(name: str, task: str, schedule: schedules.schedule | TzAwareCrontab):
        schedule = schedules.maybe_schedule(schedule)

        async with async_db_session() as db:
            if isinstance(schedule, schedules.schedule):
                every = max(schedule.run_every.total_seconds(), 0)
                spec = {
                    'name': name,
                    'type': TaskSchedulerType.INTERVAL.value,
                    'interval_every': every,
                    'interval_period': PeriodType.SECONDS.value,
                }
                stmt = select(TaskScheduler).filter_by(**spec)
                query = await db.execute(stmt)
                obj = query.scalars().first()
                if not obj:
                    obj = TaskScheduler(**CreateTaskSchedulerParam(task=task, **spec).model_dump())
            elif isinstance(schedule, schedules.crontab):
                spec = {
                    'name': name,
                    'type': TaskSchedulerType.CRONTAB.value,
                    'crontab_minute': schedule._orig_minute
                    if crontab_verify('m', schedule._orig_minute, False)
                    else '*',
                    'crontab_hour': schedule._orig_hour if crontab_verify('h', schedule._orig_hour, False) else '*',
                    'crontab_day_of_week': schedule._orig_day_of_week
                    if crontab_verify('dom', schedule._orig_day_of_week, False)
                    else '*',
                    'crontab_day_of_month': schedule._orig_day_of_month
                    if crontab_verify('dom', schedule._orig_day_of_month, False)
                    else '*',
                    'crontab_month_of_year': schedule._orig_month_of_year
                    if crontab_verify('moy', schedule._orig_month_of_year, False)
                    else '*',
                }
                stmt = select(TaskScheduler).filter_by(**spec)
                query = await db.execute(stmt)
                obj = query.scalars().first()
                if not obj:
                    obj = TaskScheduler(**CreateTaskSchedulerParam(task=task, **spec).model_dump())
            else:
                raise errors.NotFoundError(msg=f'暂不支持的计划类型：{schedule}')

            return obj

    @classmethod
    async def _unpack_fields(
        cls,
        name: str,
        task: str,
        schedule: schedules.schedule | TzAwareCrontab,
        args: tuple | None = None,
        kwargs: dict | None = None,
        options: dict = None,
        **entry,
    ) -> dict:
        model_schedule = await cls.to_model_schedule(name, task, schedule)
        model_dict = select_as_dict(model_schedule)
        for k in ['id', 'created_time', 'updated_time']:
            try:
                del model_dict[k]
            except KeyError:
                continue
        model_dict.update(
            args=json.dumps(args or []),
            kwargs=json.dumps(kwargs or {}),
            **cls._unpack_options(**options or {}),
            **entry,
        )
        return model_dict

    @classmethod
    def _unpack_options(
        cls,
        queue: str = None,
        exchange: str = None,
        routing_key: str = None,
        start_time: datetime = None,
        expires: datetime = None,
        expire_seconds: int = None,
        one_off: bool = False,
    ) -> dict:
        data = {
            'queue': queue,
            'exchange': exchange,
            'routing_key': routing_key,
            'start_time': start_time,
            'expire_time': expires,
            'expire_seconds': expire_seconds,
            'one_off': one_off,
        }
        if expires:
            if isinstance(expires, int):
                data['expire_seconds'] = expires
            elif isinstance(expires, timedelta):
                data['expire_time'] = timezone.now() + expires
        return data


class DatabaseScheduler(Scheduler):
    Entry = ModelEntry

    _schedule = None
    _last_update = None
    _initial_read = True
    _heap_invalidated = False

    def __init__(self, *args, **kwargs):
        self.app = kwargs['app']
        self._dirty = set()
        super().__init__(*args, **kwargs)
        self._finalize = Finalize(self, self.sync, exitpriority=5)
        self.max_interval = kwargs.get('max_interval') or self.app.conf.beat_max_loop_interval or DEFAULT_MAX_INTERVAL

    def setup_schedule(self):
        """重写父函数"""
        logger.info('setup_schedule')
        tasks = self.schedule
        self.install_default_entries(tasks)
        self.update_from_dict(self.app.conf.beat_schedule)

    async def get_all_task_schedulers(self):
        """获取所有任务调度"""
        async with async_db_session() as db:
            logger.debug('DatabaseScheduler: Fetching database schedule')
            stmt = select(TaskScheduler).where(TaskScheduler.enabled == 1)
            query = await db.execute(stmt)
            tasks = query.scalars().all()
            s = {}
            for task in tasks:
                s[task.name] = self.Entry(task, app=self.app)
            return s

    def schedule_changed(self) -> bool:
        """任务调度变更状态"""
        now = timezone.now()
        last_update = run_await(redis_client.get)(f'{settings.CELERY_REDIS_PREFIX}:last_update')
        if not last_update:
            run_await(redis_client.set)(f'{settings.CELERY_REDIS_PREFIX}:last_update', timezone.to_str(now))
            return False

        last, ts = self._last_update, timezone.from_str(last_update)
        try:
            if ts and ts > (last if last else ts):
                return True
        finally:
            self._last_update = now

    def reserve(self, entry):
        """重写父函数"""
        new_entry = next(entry)
        # 需要按名称存储条目，因为条目可能会发生变化
        self._dirty.add(new_entry.name)
        return new_entry

    def sync(self):
        """重写父函数"""
        _tried = set()
        _failed = set()
        try:
            while self._dirty:
                name = self._dirty.pop()
                try:
                    tasks = self.schedule
                    run_await(tasks[name].save)()
                    logger.debug(f'保存任务 {name} 最新状态到数据库')
                    _tried.add(name)
                except KeyError as e:
                    logger.error(f'保存任务 {name} 最新状态失败：{e} ')
                    _failed.add(name)
        except DatabaseError as e:
            logger.exception('同步时出现数据库错误: %r', e)
        except InterfaceError as e:
            logger.warning(f'DatabaseScheduler InterfaceError：{str(e)}，等待下次调用时重试...')
        finally:
            # 请稍后重试（仅针对失败的）
            self._dirty |= _failed

    def update_from_dict(self, beat_dict: dict):
        """重写父函数"""
        s = {}
        for name, entry_fields in beat_dict.items():
            try:
                entry = run_await(self.Entry.from_entry)(name, app=self.app, **entry_fields)
                if entry.model.enabled:
                    s[name] = entry
            except Exception as e:
                logger.error(f'添加任务 {name} 到数据库失败')
                raise e

        tasks = self.schedule
        tasks.update(s)

    def install_default_entries(self, data):
        """重写父函数"""
        entries = {}
        if self.app.conf.result_expires:
            entries.setdefault(
                'celery.backend_cleanup',
                {
                    'task': 'celery.backend_cleanup',
                    'schedule': schedules.crontab('0', '4', '*'),
                    'options': {'expire_seconds': 12 * 3600},
                },
            )
        self.update_from_dict(entries)

    def schedules_equal(self, *args, **kwargs):
        """重写父函数"""
        if self._heap_invalidated:
            self._heap_invalidated = False
            return False
        return super().schedules_equal(*args, **kwargs)

    @property
    def schedule(self) -> dict[str, ModelEntry]:
        """获取任务调度"""
        initial = update = False
        if self._initial_read:
            logger.debug('DatabaseScheduler: initial read')
            initial = update = True
            self._initial_read = False
        elif self.schedule_changed():
            logger.info('DatabaseScheduler: Schedule changed.')
            update = True

        if update:
            logger.debug('beat: Synchronizing schedule...')
            self.sync()
            self._schedule = run_await(self.get_all_task_schedulers)()
            # 计划已更改，使 Scheduler.tick 中的堆无效
            if not initial:
                self._heap = []
                self._heap_invalidated = True
            logger.debug(
                'Current schedule:\n%s',
                '\n'.join(repr(entry) for entry in self._schedule.values()),
            )

        # logger.debug(self._schedule)
        return self._schedule
