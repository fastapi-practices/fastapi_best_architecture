from datetime import datetime

from celery import schedules
from celery.schedules import ParseException, crontab

from backend.common.exception import errors
from backend.utils.timezone import timezone


class TzAwareCrontab(schedules.crontab):
    """时区感知 Crontab"""

    def __init__(self, minute='*', hour='*', day_of_week='*', day_of_month='*', month_of_year='*', app=None) -> None:  # noqa: ANN001
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


def crontab_verify(crontab_str: str) -> None:
    """
    验证 Celery crontab 表达式

    :param crontab_str: 计划表达式
    :return:
    """
    crontab_split = crontab_str.split(' ')
    if len(crontab_split) != 5:
        raise errors.RequestError(msg='Crontab 表达式非法')
    try:
        crontab(*crontab_split)
    except ParseException:
        raise errors.RequestError(msg='Crontab 表达式非法')
