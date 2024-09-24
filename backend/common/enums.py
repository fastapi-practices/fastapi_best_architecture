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


class GenModelMySQLColumnType(StrEnum):
    """代码生成模型列类型（MySQL）"""

    # Python 类型映射
    BIGINT = 'int'
    BigInteger = 'int'  # BIGINT
    BINARY = 'bytes'
    BLOB = 'bytes'
    BOOLEAN = 'bool'  # BOOL
    Boolean = 'bool'  # BOOL
    CHAR = 'str'
    CLOB = 'str'
    DATE = 'date'
    Date = 'date'  # DATE
    DATETIME = 'datetime'
    DateTime = 'datetime'  # DATETIME
    DECIMAL = 'Decimal'
    DOUBLE = 'float'
    Double = 'float'  # DOUBLE
    DOUBLE_PRECISION = 'float'
    Enum = 'Enum'  # Enum()
    FLOAT = 'float'
    Float = 'float'  # FLOAT
    INT = 'int'  # INTEGER
    INTEGER = 'int'
    Integer = 'int'  # INTEGER
    Interval = 'timedelta'  # DATETIME
    JSON = 'dict'
    LargeBinary = 'bytes'  # BLOB
    NCHAR = 'str'
    NUMERIC = 'Decimal'
    Numeric = 'Decimal'  # NUMERIC
    NVARCHAR = 'str'  # String
    PickleType = 'bytes'  # BLOB
    REAL = 'float'
    SMALLINT = 'int'
    SmallInteger = 'int'  # SMALLINT
    String = 'str'  # String
    TEXT = 'str'
    Text = 'str'  # TEXT
    TIME = 'time'
    Time = 'time'  # TIME
    TIMESTAMP = 'datetime'
    Unicode = 'str'  # String
    UnicodeText = 'str'  # TEXT
    UUID = 'str | UUID'
    Uuid = 'str'  # CHAR(32)
    VARBINARY = 'bytes'
    VARCHAR = 'str'  # String

    # sa.dialects.mysql 导入
    BIT = 'bool'
    ENUM = 'Enum'
    LONGBLOB = 'bytes'
    LONGTEXT = 'str'
    MEDIUMBLOB = 'bytes'
    MEDIUMINT = 'int'
    MEDIUMTEXT = 'str'
    SET = 'list[str]'
    TINYBLOB = 'bytes'
    TINYINT = 'int'
    TINYTEXT = 'str'
    YEAR = 'int'


class GenModelPostgreSQLColumnType(StrEnum):
    """代码生成模型列类型（PostgreSQL），仅作为数据保留，并未实施"""

    # Python 类型映射
    BIGINT = 'int'
    BigInteger = 'int'  # BIGINT
    BINARY = 'bytes'
    BLOB = 'bytes'
    BOOLEAN = 'bool'
    Boolean = 'bool'  # BOOLEAN
    CHAR = 'str'
    CLOB = 'str'
    DATE = 'date'
    Date = 'date'  # DATE
    DATETIME = 'datetime'
    DateTime = 'datetime'  # TIMESTAMP WITHOUT TIME ZONE
    DECIMAL = 'Decimal'
    DOUBLE = 'float'
    Double = 'float'  # DOUBLE PRECISION
    DOUBLE_PRECISION = 'float'  # DOUBLE PRECISION
    Enum = 'Enum'  # Enum(name='enum')
    FLOAT = 'float'
    Float = 'float'  # FLOAT
    INT = 'int'  # INTEGER
    INTEGER = 'int'
    Integer = 'int'  # INTEGER
    Interval = 'timedelta'  # INTERVAL
    JSON = 'dict'
    LargeBinary = 'bytes'  # BYTEA
    NCHAR = 'str'
    NUMERIC = 'Decimal'
    Numeric = 'Decimal'  # NUMERIC
    NVARCHAR = 'str'  # String
    PickleType = 'bytes'  # BYTEA
    REAL = 'float'
    SMALLINT = 'int'
    SmallInteger = 'int'  # SMALLINT
    String = 'str'  # String
    TEXT = 'str'
    Text = 'str'  # TEXT
    TIME = 'time'  # TIME WITHOUT TIME ZONE
    Time = 'time'  # TIME WITHOUT TIME ZONE
    TIMESTAMP = 'datetime'  # TIMESTAMP WITHOUT TIME ZONE
    Unicode = 'str'  # String
    UnicodeText = 'str'  # TEXT
    UUID = 'str | UUID'
    Uuid = 'str'
    VARBINARY = 'bytes'
    VARCHAR = 'str'  # String

    # sa.dialects.postgresql 导入
    ARRAY = 'list'
    BIT = 'bool'
    BYTEA = 'bytes'
    CIDR = 'str'
    CITEXT = 'str'
    DATEMULTIRANGE = 'list[date]'
    DATERANGE = 'tuple[date, date]'
    DOMAIN = 'str'
    ENUM = 'Enum'
    HSTORE = 'dict'
    INET = 'str'
    INT4MULTIRANGE = 'list[int]'
    INT4RANGE = 'tuple[int, int]'
    INT8MULTIRANGE = 'list[int]'
    INT8RANGE = 'tuple[int, int]'
    INTERVAL = 'timedelta'
    JSONB = 'dict'
    JSONPATH = 'str'
    MACADDR = 'str'
    MACADDR8 = 'str'
    MONEY = 'Decimal'
    NUMMULTIRANGE = 'list[Decimal]'
    NUMRANGE = 'tuple[Decimal, Decimal]'
    OID = 'int'
    REGCLASS = 'str'
    REGCONFIG = 'str'
    TSMULTIRANGE = 'list[datetime]'
    TSQUERY = 'str'
    TSRANGE = 'tuple[datetime, datetime]'
    TSTZMULTIRANGE = 'list[datetime]'
    TSTZRANGE = 'tuple[datetime, datetime]'
    TSVECTOR = 'str'
