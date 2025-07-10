#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Literal

from celery import schedules
from celery.schedules import ParseException, crontab_parser

from backend.common.exception import errors
from backend.utils.timezone import timezone


class TzAwareCrontab(schedules.crontab):
    """时区感知 Crontab"""

    def __init__(self, minute='*', hour='*', day_of_week='*', day_of_month='*', month_of_year='*', app=None):
        super().__init__(
            minute=minute,
            hour=hour,
            day_of_week=day_of_week,
            day_of_month=day_of_month,
            month_of_year=month_of_year,
            nowfun=timezone.now,
            app=app,
        )

    def is_due(self, last_run_at: datetime) -> tuple[bool, int | float]:
        """
        任务到期状态

        :param last_run_at: 最后运行时间
        :return:
        """
        rem_delta = self.remaining_estimate(last_run_at)
        rem = max(rem_delta.total_seconds(), 0)
        due = rem == 0
        if due:
            rem_delta = self.remaining_estimate(self.now())
            rem = max(rem_delta.total_seconds(), 0)
        return schedules.schedstate(is_due=due, next=rem)

    def __reduce__(self) -> tuple[type, tuple[str, str, str, str, str], None]:
        return (
            self.__class__,
            (
                self._orig_minute,
                self._orig_hour,
                self._orig_day_of_week,
                self._orig_day_of_month,
                self._orig_month_of_year,
            ),
            None,
        )


def crontab_verify(filed: Literal['m', 'h', 'dow', 'dom', 'moy'], value: str, raise_exc: bool = True) -> bool:
    """
    验证 Celery crontab 表达式

    :param filed: 验证的字段
    :param value: 验证的值
    :param raise_exc: 是否抛出异常
    :return:
    """
    valid = True

    try:
        match filed:
            case 'm':
                crontab_parser(60, 0).parse(value)
            case 'h':
                crontab_parser(24, 0).parse(value)
            case 'dow':
                crontab_parser(7, 0).parse(value)
            case 'dom':
                crontab_parser(31, 1).parse(value)
            case 'moy':
                crontab_parser(12, 1).parse(value)
            case _:
                raise errors.ServerError(msg=f'无效字段：{filed}')
    except ParseException:
        valid = False
        if raise_exc:
            raise errors.RequestError(msg=f'crontab 值 {value} 非法')

    return valid
