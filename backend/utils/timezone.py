#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import zoneinfo

from datetime import datetime
from datetime import timezone as datetime_timezone

from backend.core.conf import settings


class TimeZone:
    def __init__(self, tz: str = settings.DATETIME_TIMEZONE) -> None:
        """
        Initialization Timezone Converter

        :param tz: Time zone name, default is settings. DATETIME_TIMEZONE
        :return:
        """
        self.tz_info = zoneinfo.ZoneInfo(tz)

    def now(self) -> datetime:
        """Get Current Timezone"""
        return datetime.now(self.tz_info)

    def f_datetime(self, dt: datetime) -> datetime:
        """
        convert datetime object to current time zone

        :param dt: datatime objects to convert
        :return:
        """
        return dt.astimezone(self.tz_info)

    def f_str(self, date_str: str, format_str: str = settings.DATETIME_FORMAT) -> datetime:
        """
        convert time string to current time zone datetime object

        :param date_str: time string
        :param format_str: Time format string, default is settings. DATETIME_FORMAT
        :return:
        """
        return datetime.strptime(date_str, format_str).replace(tzinfo=self.tz_info)

    @staticmethod
    def t_str(dt: datetime, format_str: str = settings.DATETIME_FORMAT) -> str:
        """
        convert datetime objects to a time string in a specified format

        :param dt: datetime objects
        :param format_str: Time format string, default is settings. DATETIME_FORMAT
        :return:
        """
        return dt.strftime(format_str)

    @staticmethod
    def f_utc(dt: datetime) -> datetime:
        """
        Convert datetime object to UTC (GMT) time slot

        :param dt: datatime objects to convert
        :return:
        """
        return dt.astimezone(datetime_timezone.utc)


timezone: TimeZone = TimeZone()
