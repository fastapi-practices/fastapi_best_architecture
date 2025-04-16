#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.core.conf import settings
from backend.plugin.code_generator.enums import GenModelMySQLColumnType, GenModelPostgreSQLColumnType


def sql_type_to_sqlalchemy(typing: str) -> str:
    """
    将 SQL 类型转换为 SQLAlchemy 类型

    :param typing: SQL 类型字符串
    :return:
    """
    if settings.DATABASE_TYPE == 'mysql':
        if typing in GenModelMySQLColumnType.get_member_keys():
            return typing
    else:
        if typing in GenModelPostgreSQLColumnType.get_member_keys():
            return typing
    return 'String'


def sql_type_to_pydantic(typing: str) -> str:
    """
    将 SQL 类型转换为 Pydantic 类型

    :param typing: SQL 类型字符串
    :return:
    """
    try:
        if settings.DATABASE_TYPE == 'mysql':
            return GenModelMySQLColumnType[typing].value
        if typing == 'CHARACTER VARYING':  # postgresql 中 DDL VARCHAR 的别名
            return 'str'
        return GenModelPostgreSQLColumnType[typing].value
    except KeyError:
        return 'str'
