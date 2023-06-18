#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import pytz

from backend.app.core.conf import settings


class DateTimeUtils:
    def __init__(self, timezone_str=settings.DATETIME_TIMEZONE):
        """
        初始化函数，设置时区

        :param timezone_str: 时区字符串，默认为 UTC
        """
        self.timezone_str = timezone_str
        self.timezone = pytz.timezone(self.timezone_str)

    def get_current_time(self) -> datetime.datetime:
        """
        获取当前时间

        :return: 当前时间的 datetime 对象
        """
        return datetime.datetime.now(self.timezone)

    @staticmethod
    def get_current_timestamp() -> int:
        """
        获取当前时间戳 (秒)

        :return: 当前时间戳 (秒)
        """
        return int(datetime.datetime.now().timestamp())

    @staticmethod
    def get_current_milliseconds() -> int:
        """
        获取当前时间戳 (毫秒)

        :return: 当前时间戳 (毫秒)
        """
        return int(datetime.datetime.now().timestamp() * 1000)

    def timestamp_to_datetime(self, timestamp: int) -> datetime.datetime:
        """
        时间戳转 datetime 对象

        :param timestamp: 时间戳 (秒)
        :return: datetime 对象
        """
        return datetime.datetime.utcfromtimestamp(timestamp).replace(tzinfo=self.timezone)

    def datetime_to_timestamp(self, dt: datetime.datetime) -> int:
        """
        datetime 对象转时间戳（秒）

        :param dt: datetime 对象
        :return: 时间戳 (秒)
        """
        return int(dt.astimezone(self.timezone).timestamp())

    def datetime_to_milliseconds(self, dt: datetime.datetime) -> int:
        """
        datetime 对象转时间戳（毫秒）

        :param dt: datetime 对象
        :return: 时间戳 (毫秒)
        """
        return int(dt.astimezone(self.timezone).timestamp() * 1000)

    def str_to_datetime(self, time_str: str, format_str: str = settings.DATETIME_FORMAT) -> datetime.datetime:
        """
        时间字符串转 datetime 对象

        :param time_str: 时间字符串
        :param format_str: 时间字符串的格式，默认为 '%Y-%m-%d %H:%M:%S'
        :return: datetime 对象
        """
        return datetime.datetime.strptime(time_str, format_str).replace(tzinfo=self.timezone)

    def datetime_to_str(self, dt: datetime.datetime, format_str: str = settings.DATETIME_FORMAT) -> str:
        """
        datetime 对象转时间字符串

        :param dt: datetime 对象
        :param format_str: 时间字符串的格式，默认为 '%Y-%m-%d %H:%M:%S'
        :return: 时间字符串
        """
        return dt.astimezone(self.timezone).strftime(format_str)

    @staticmethod
    def get_timezone(timezone_str: str) -> pytz.timezone:
        """
        获取指定时区的 pytz.timezone 对象

        :param timezone_str: 时区字符串
        :return: pytz.timezone 对象
        """
        return pytz.timezone(timezone_str)

    def get_timezone_time(self, timezone_str: str) -> datetime.datetime:
        """
        获取指定时区的当前时间

        :param timezone_str: 时区字符串
        :return: 当前时间的 datetime 对象
        """
        timezone = self.get_timezone(timezone_str)
        return datetime.datetime.now(timezone)

    def datetime_to_timezone(self, dt: datetime.datetime, timezone_str: str) -> datetime.datetime:
        """
        将 datetime 对象转换为指定时区的 datetime 对象

        :param dt: datetime 对象
        :param timezone_str: 目标时区字符串
        :return: 目标时区的 datetime 对象
        """
        timezone = self.get_timezone(timezone_str)
        return dt.astimezone(timezone)

    def datetime_to_timezone_str(
        self, dt: datetime.datetime, timezone_str: str, format_str: str = settings.DATETIME_FORMAT
    ) -> str:
        """
        将 datetime 对象转换为指定时区的时间字符串

        :param dt: datetime 对象
        :param timezone_str: 目标时区字符串
        :param format_str: 时间字符串的格式，默认为 '%Y-%m-%d %H:%M:%S'
        :return: 目标时区的时间字符串
        """
        dt_timezone = self.datetime_to_timezone(dt, timezone_str)
        return dt_timezone.strftime(format_str)

    def str_to_timezone(
        self, time_str: str, timezone_str: str, format_str: str = settings.DATETIME_FORMAT
    ) -> datetime.datetime:
        """
        将指定时区的时间字符串转换为 datetime 对象

        :param time_str: 指定时区的时间字符串
        :param timezone_str: 指定时区字符串
        :param format_str: 时间字符串的格式，默认为 '%Y-%m-%d %H:%M:%S'
        :return: datetime 对象
        """
        dt = datetime.datetime.strptime(time_str, format_str).replace(tzinfo=self.timezone)
        return self.datetime_to_timezone(dt, timezone_str)

    @staticmethod
    def datetime_to_utc(dt: datetime.datetime) -> datetime.datetime:
        """
        将 datetime 对象转换为 UTC 时间

        :param dt: datetime 对象
        :return: UTC 时间的 datetime 对象
        """
        return dt.astimezone(pytz.utc)

    def str_to_utc(self, time_str: str, format_str: str = settings.DATETIME_FORMAT) -> datetime.datetime:
        """
        将时间字符串转换为 UTC 时间的 datetime 对象

        :param time_str: 时间字符串
        :param format_str: 时间字符串的格式，默认为 '%Y-%m-%d %H:%M:%S'
        :return: UTC 时间的 datetime 对象
        """
        dt = datetime.datetime.strptime(time_str, format_str).replace(tzinfo=self.timezone)
        return self.datetime_to_utc(dt)

    def utc_to_datetime(self, utc_time: datetime.datetime) -> datetime.datetime:
        """
        将 UTC 时间的 datetime 对象转换为指定时区的 datetime 对象

        :param utc_time: UTC 时间的 datetime 对象
        :return: 目标时区的 datetime 对象
        """
        return utc_time.replace(tzinfo=pytz.utc).astimezone(self.timezone).replace(tzinfo=None)

    def get_expire_time(self, expires_delta: datetime.timedelta) -> datetime:
        """
        获取过期时间

        :param expires_delta: 时间间隔对象
        :return: 过期时间的 datetime 对象
        """
        return self.get_current_time() + expires_delta

    @staticmethod
    def get_expire_time_from_datetime(expire_time: datetime, seconds: int) -> datetime:
        """
        获取从指定时间开始一定时间后的过期时间

        :param expire_time: 指定时间的 datetime 对象
        :param seconds: 时间间隔（秒）
        :return: 过期时间的 datetime 对象
        """
        return expire_time + datetime.timedelta(seconds=seconds)

    @staticmethod
    def get_expire_seconds(expires_delta: datetime.timedelta) -> int:
        """
        获取过期时间（秒）

        :param expires_delta: 时间间隔对象
        :return: 过期时间（秒）
        """
        return int(expires_delta.total_seconds())

    def get_expire_seconds_from_datetime(self, expire_datetime: datetime) -> int:
        """
        获取从指定时间开始到当前时间的时间间隔（秒）

        :param expire_datetime: 指定时间的 datetime 对象
        :return: 时间间隔（秒）
        """
        current_time = self.get_current_time()
        if expire_datetime < current_time:
            return 0
        return int((expire_datetime - current_time).total_seconds())


datetime_utils = DateTimeUtils()
