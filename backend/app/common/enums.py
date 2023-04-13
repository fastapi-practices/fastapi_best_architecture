#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum


class EnumBase(Enum):

    @classmethod
    def get_member_values(cls):
        return [item.value for item in cls._member_map_.values()]

    @classmethod
    def get_member_names(cls):
        return [name for name in cls._member_names_]


class IntEnum(int, EnumBase):
    """整型枚举"""
    pass


class StrEnum(str, EnumBase):
    """字符串枚举"""
    pass
