#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime

import pytz

from backend.app.core.conf import settings


class TimeZoneUtils:
    def __init__(self, timezone_str=settings.DATETIME_TIMEZONE):
        self.timezone = pytz.timezone(timezone_str)

    def get_timezone_datetime(self) -> datetime.datetime:
        """
        获取时区时间

        :return:
        """
        return datetime.datetime.now(self.timezone)

    def get_timezone_timestamp(self) -> int:
        """
        获取时区时间戳 (秒)

        :return:
        """
        return int(self.get_timezone_datetime().timestamp())

    def get_timezone_milliseconds(self) -> int:
        """
        获取时区时间戳 (毫秒)

        :return:
        """
        return int(self.get_timezone_datetime().timestamp() * 1000)

    def timestamp_to_timezone_datetime(self, timestamp: int) -> datetime.datetime:
        """
        时间戳转 datetime 时区对象

        :param timestamp:
        :return:
        """
        return datetime.datetime.utcfromtimestamp(timestamp).replace(tzinfo=self.timezone)

    def datetime_to_timezone_timestamp(self, dt: datetime.datetime) -> int:
        """
        datetime 对象转时区时间戳（秒）

        :param dt:
        :return:
        """
        return int(dt.astimezone(self.timezone).timestamp())

    def datetime_to_timezone_milliseconds(self, dt: datetime.datetime) -> int:
        """
        datetime 对象转时区时间戳（毫秒）

        :param dt:
        :return:
        """
        return int(dt.astimezone(self.timezone).timestamp() * 1000)

    def str_to_timezone_datetime(self, time_str: str, format_str: str = settings.DATETIME_FORMAT) -> datetime.datetime:
        """
        时间字符串转 datetime 时区对象

        :param time_str:
        :param format_str:
        :return:
        """
        return datetime.datetime.strptime(time_str, format_str).replace(tzinfo=self.timezone)

    def datetime_to_timezone_str(self, dt: datetime.datetime, format_str: str = settings.DATETIME_FORMAT) -> str:
        """
        datetime 对象转时区时间字符串

        :param dt:
        :param format_str:
        :return:
        """
        return dt.astimezone(self.timezone).strftime(format_str)

    def datetime_to_timezone_datetime(self, dt: datetime.datetime) -> datetime.datetime:
        """
        datetime 对象转 datetime 时区对象

        :param dt:
        :return:
        """
        return dt.astimezone(self.timezone)

    @staticmethod
    def datetime_to_timezone_utc(dt: datetime.datetime) -> datetime.datetime:
        """
        datetime 对象转 datetime UTC 对象

        :param dt:
        :return:
        """
        return dt.astimezone(pytz.utc)

    def str_to_timezone_utc(self, time_str: str, format_str: str = settings.DATETIME_FORMAT) -> datetime.datetime:
        """
        时间字符串转时区 datetime UTC 对象

        :param time_str:
        :param format_str:
        :return:
        """
        dt = datetime.datetime.strptime(time_str, format_str).replace(tzinfo=self.timezone)
        return self.datetime_to_timezone_utc(dt)

    def utc_to_timezone_datetime(self, utc_time: datetime.datetime) -> datetime.datetime:
        """
        datetime UTC 对象转 datetime 时区对象

        :param utc_time:
        :return:
        """
        return utc_time.replace(tzinfo=pytz.utc).astimezone(self.timezone)

    def get_timezone_expire_time(self, expires_delta: datetime.timedelta) -> datetime.datetime:
        """
        获取时区过期时间

        :param expires_delta:
        :return:
        """
        return self.get_timezone_datetime() + expires_delta

    def get_timezone_expire_seconds(self, expire_datetime: datetime.datetime) -> int:
        """
        获取从指定时间开始到当前时间的时间间隔（秒）

        :param expire_datetime: 指定时间的 datetime 对象
        :return: 时间间隔（秒）
        """
        timezone_datetime = self.get_timezone_datetime()
        expire_datetime = self.datetime_to_timezone_datetime(expire_datetime)
        if expire_datetime < timezone_datetime:
            return 0
        return int((expire_datetime - timezone_datetime).total_seconds())


timezone_utils = TimeZoneUtils()
