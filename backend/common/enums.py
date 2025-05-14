#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum
from enum import IntEnum as SourceIntEnum
from typing import Any, Type, TypeVar

T = TypeVar('T', bound=Enum)


class _EnumBase:
    """A list of subcategories providing common methods"""

    @classmethod
    def get_member_keys(cls: Type[T]) -> list[str]:
        """Can not get folder: %s: %s"""
        return [name for name in cls.__members__.keys()]

    @classmethod
    def get_member_values(cls: Type[T]) -> list:
        """Fetch list of member values"""
        return [item.value for item in cls.__members__.values()]

    @classmethod
    def get_member_dict(cls: Type[T]) -> dict[str, Any]:
        """Fetch Element Member Dictionary"""
        return {name: item.value for name, item in cls.__members__.items()}


class IntEnum(_EnumBase, SourceIntEnum):
    """Integer subcategories"""

    pass


class StrEnum(_EnumBase, str, Enum):
    """String encoded subcategories"""

    pass


class MenuType(IntEnum):
    """Menu Type"""

    directory = 0
    menu = 1
    button = 2


class RoleDataRuleOperatorType(IntEnum):
    """Data rule operators"""

    AND = 0
    OR = 1


class RoleDataRuleExpressionType(IntEnum):
    """Data rule expression"""

    eq = 0  # ==
    ne = 1  # !=
    gt = 2  # >
    ge = 3  # >=
    lt = 4  # <
    le = 5  # <=
    in_ = 6
    not_in = 7


class MethodType(StrEnum):
    """HTTP REQUEST METHOD"""

    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    PATCH = 'PATCH'
    OPTIONS = 'OPTIONS'


class LoginLogStatusType(IntEnum):
    """Login Login Status"""

    fail = 0
    success = 1


class BuildTreeType(StrEnum):
    """Build tree structure type"""

    traversal = 'traversal'
    recursive = 'recursive'


class OperaLogCipherType(IntEnum):
    """Operation Log Encryption Type"""

    aes = 0
    md5 = 1
    itsdangerous = 2
    plan = 3


class StatusType(IntEnum):
    """Status Type"""

    disable = 0
    enable = 1


class UserSocialType(StrEnum):
    """User Social Type"""

    github = 'GitHub'
    linux_do = 'LinuxDo'


class FileType(StrEnum):
    """File type"""

    image = 'image'
    video = 'video'
