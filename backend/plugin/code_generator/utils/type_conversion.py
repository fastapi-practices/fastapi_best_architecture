#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.core.conf import settings
from backend.plugin.code_generator.enums import GenModelMySQLColumnType, GenModelPostgreSQLColumnType


def sql_type_to_sqlalchemy(typing: str) -> str:
    """
    Convert SQL type to SQLAlchemy type

    :param typeping: SQL type string
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
    Convert SQL type to Pydantic type

    :param typeping: SQL type string
    :return:
    """
    try:
        if settings.DATABASE_TYPE == 'mysql':
            return GenModelMySQLColumnType[typing].value
        if typing == 'CHARACTER VARYING':  # alias of DDL Varchar in postgresql
            return 'str'
        return GenModelPostgreSQLColumnType[typing].value
    except KeyError:
        return 'str'
