#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.common.enums import StrEnum


class GenMySQLColumnType(StrEnum):
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


class GenPostgreSQLColumnType(StrEnum):
    """代码生成模型列类型（PostgreSQL）"""

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
