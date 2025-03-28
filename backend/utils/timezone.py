#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import zoneinfo

from datetime import datetime
from datetime import timezone as datetime_timezone

from backend.core.conf import settings


class TimeZone:
    def __init__(self, tz: str = settings.DATETIME_TIMEZONE) -> None:
        """
        初始化时区转换器

        :param tz: 时区名称，默认为 settings.DATETIME_TIMEZONE
        :return:
        """
        self.tz_info = zoneinfo.ZoneInfo(tz)

    def now(self) -> datetime:
        """获取当前时区时间"""
        return datetime.now(self.tz_info)

    def f_datetime(self, dt: datetime) -> datetime:
        """
        将 datetime 对象转换为当前时区时间

        :param dt: 需要转换的 datetime 对象
        :return:
        """
        return dt.astimezone(self.tz_info)

    def f_str(self, date_str: str, format_str: str = settings.DATETIME_FORMAT) -> datetime:
        """
        将时间字符串转换为当前时区的 datetime 对象

        :param date_str: 时间字符串
        :param format_str: 时间格式字符串，默认为 settings.DATETIME_FORMAT
        :return:
        """
        return datetime.strptime(date_str, format_str).replace(tzinfo=self.tz_info)

    @staticmethod
    def t_str(dt: datetime, format_str: str = settings.DATETIME_FORMAT) -> str:
        """
        将 datetime 对象转换为指定格式的时间字符串

        :param dt: datetime 对象
        :param format_str: 时间格式字符串，默认为 settings.DATETIME_FORMAT
        :return:
        """
        return dt.strftime(format_str)

    @staticmethod
    def f_utc(dt: datetime) -> datetime:
        """
        将 datetime 对象转换为 UTC (GMT) 时区时间

        :param dt: 需要转换的 datetime 对象
        :return:
        """
        return dt.astimezone(datetime_timezone.utc)


timezone: TimeZone = TimeZone()
