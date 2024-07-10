#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum
from enum import IntEnum as SourceIntEnum
from typing import Type


class _EnumBase:
    @classmethod
    def get_member_keys(cls: Type[Enum]) -> list[str]:
        return [name for name in cls.__members__.keys()]

    @classmethod
    def get_member_values(cls: Type[Enum]) -> list:
        return [item.value for item in cls.__members__.values()]


class IntEnum(_EnumBase, SourceIntEnum):
    """整型枚举"""

    pass


class StrEnum(_EnumBase, str, Enum):
    """字符串枚举"""

    pass


class MenuType(IntEnum):
    """菜单类型"""

    directory = 0
    menu = 1
    button = 2


class RoleDataScopeType(IntEnum):
    """数据范围"""

    all = 1
    custom = 2


class MethodType(StrEnum):
    """请求方法"""

    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    PATCH = 'PATCH'
    OPTIONS = 'OPTIONS'


class LoginLogStatusType(IntEnum):
    """登陆日志状态"""

    fail = 0
    success = 1


class BuildTreeType(StrEnum):
    """构建树形结构类型"""

    traversal = 'traversal'
    recursive = 'recursive'


class OperaLogCipherType(IntEnum):
    """操作日志加密类型"""

    aes = 0
    md5 = 1
    itsdangerous = 2
    plan = 3


class StatusType(IntEnum):
    """状态类型"""

    disable = 0
    enable = 1


class UserSocialType(StrEnum):
    """用户社交类型"""

    github = 'GitHub'
    linuxdo = 'LinuxDo'


class GenModelType(StrEnum):
    """代码生成模型类型"""

    # 待优化
    # https://github.com/zy7y/dfs-generate/blob/master/dfs_generate/types_map.py
    ARRAY = 'array'
    BIGINT = 'bigint'
    BigInteger = 'biginteger'
    BINARY = 'binary'
    BLOB = 'blob'
    BOOLEAN = 'boolean'
    Boolean = 'boolean'
    CHAR = 'char'
    CLOB = 'clob'
    DATE = 'date'
    Date = 'date'
    DATETIME = 'datetime'
    DateTime = 'datetime'
    DECIMAL = 'decimal'
    DOUBLE = 'double'
    Double = 'double'
    DOUBLE_PRECISION = 'double_precision'
    Enum = 'enum'
    FLOAT = 'float'
    Float = 'float'
    INT = 'int'
    INTEGER = 'integer'
    Integer = 'integer'
    Interval = 'interval'
    JSON = 'json'
    LargeBinary = 'largebinary'
    LONGTEXT = 'longtext'
    NCHAR = 'nchar'
    NUMERIC = 'numeric'
    Numeric = 'numeric'
    NVARCHAR = 'nvarchar'
    PickleType = 'pickletype'
    REAL = 'real'
    SMALLINT = 'smallint'
    SmallInteger = 'smallinteger'
    String = 'string'
    TEXT = 'text'
    Text = 'text'
    TIME = 'time'
    Time = 'time'
    TIMESTAMP = 'timestamp'
    TupleType = 'tupletype'
    TypeDecorator = 'typedecorator'
    Unicode = 'unicode'
    UnicodeText = 'unicodetext'
    UUID = 'uuid'
    Uuid = 'uuid'
    VARBINARY = 'varbinary'
    VARCHAR = 'varchar'
