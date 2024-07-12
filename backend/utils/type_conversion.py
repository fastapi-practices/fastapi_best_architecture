#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.common.enums import GenModelColumnType


def sql_type_to_sqlalchemy(typing: str) -> str:
    """
    Converts a sql type to a SQLAlchemy type.

    :param typing:
    :return:
    """
    type_mapping = {
        GenModelColumnType.BIGINT: 'BIGINT',
        GenModelColumnType.BINARY: 'BINARY',
        GenModelColumnType.BIT: 'BIT',
        GenModelColumnType.BLOB: 'BLOG',
        GenModelColumnType.BOOL: 'BOOLEAN',
        GenModelColumnType.BOOLEAN: 'BOOLEAN',
        GenModelColumnType.CHAR: 'CHAR',
        GenModelColumnType.DATE: 'DATE',
        GenModelColumnType.DATETIME: 'DATETIME',
        GenModelColumnType.DECIMAL: 'DECIMAL',
        GenModelColumnType.DOUBLE: 'DOUBLE',
        GenModelColumnType.ENUM: 'ENUM',
        GenModelColumnType.FLOAT: 'FLOAT',
        GenModelColumnType.INT: 'INT',
        GenModelColumnType.INTEGER: 'INTEGER',
        GenModelColumnType.JSON: 'JSON',
        GenModelColumnType.LONGBLOB: 'LONGBLOB',
        GenModelColumnType.LONGTEXT: 'LONGTEXT',
        GenModelColumnType.MEDIUMBLOB: 'MEDIUMBLOB',
        GenModelColumnType.MEDIUMINT: 'MEDIUMINT',
        GenModelColumnType.MEDIUMTEXT: 'MEDIUMTEXT',
        GenModelColumnType.NUMERIC: 'NUMERIC',
        GenModelColumnType.SET: 'SET',
        GenModelColumnType.SMALLINT: 'SMALLINT',
        GenModelColumnType.REAL: 'REAL',
        GenModelColumnType.TEXT: 'TEXT',
        GenModelColumnType.TIME: 'TIME',
        GenModelColumnType.TIMESTAMP: 'TIMESTAMP',
        GenModelColumnType.TINYBLOB: 'TINYBLOB',
        GenModelColumnType.TINYINT: 'TINYINT',
        GenModelColumnType.TINYTEXT: 'TINYTEXT',
        GenModelColumnType.VARBINARY: 'VARBINARY',
        GenModelColumnType.VARCHAR: 'String',
        GenModelColumnType.YEAR: 'YEAR',
    }
    return type_mapping.get(typing, 'String')


def sql_type_to_pydantic(typing: str) -> str:
    """
    Converts a sql type to a pydantic type.

    :param typing:
    :return:
    """
    type_mapping = {
        GenModelColumnType.BIGINT: 'int',
        GenModelColumnType.BINARY: 'bytes',
        GenModelColumnType.BIT: 'bool',
        GenModelColumnType.BLOB: 'bytes',
        GenModelColumnType.BOOL: 'bool',
        GenModelColumnType.BOOLEAN: 'bool',
        GenModelColumnType.CHAR: 'str',
        GenModelColumnType.DATE: 'date',
        GenModelColumnType.DATETIME: 'datetime',
        GenModelColumnType.DECIMAL: 'Decimal',
        GenModelColumnType.DOUBLE: 'float',
        GenModelColumnType.ENUM: 'Enum',
        GenModelColumnType.FLOAT: 'float',
        GenModelColumnType.INT: 'int',
        GenModelColumnType.INTEGER: 'int',
        GenModelColumnType.JSON: 'dict',
        GenModelColumnType.LONGBLOB: 'bytes',
        GenModelColumnType.LONGTEXT: 'str',
        GenModelColumnType.MEDIUMBLOB: 'bytes',
        GenModelColumnType.MEDIUMINT: 'int',
        GenModelColumnType.MEDIUMTEXT: 'str',
        GenModelColumnType.NUMERIC: 'NUMERIC',
        GenModelColumnType.SET: 'List[str]',
        GenModelColumnType.SMALLINT: 'int',
        GenModelColumnType.REAL: 'float',
        GenModelColumnType.TEXT: 'str',
        GenModelColumnType.TIME: 'time',
        GenModelColumnType.TIMESTAMP: 'datetime',
        GenModelColumnType.TINYBLOB: 'bytes',
        GenModelColumnType.TINYINT: 'int',
        GenModelColumnType.TINYTEXT: 'str',
        GenModelColumnType.VARBINARY: 'bytes',
        GenModelColumnType.VARCHAR: 'str',
        GenModelColumnType.YEAR: 'int',
    }
    return type_mapping.get(typing, 'str')
