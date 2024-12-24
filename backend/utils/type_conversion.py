#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.common.enums import GenModelMySQLColumnType, GenModelPostgreSQLColumnType
from backend.core.conf import settings


def sql_type_to_sqlalchemy(typing: str) -> str:
    """
    Converts a sql type to a SQLAlchemy type.

    :param typing:
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
    Converts a sql type to a pydantic type.

    :param typing:
    :return:
    """
    try:
        if settings.DATABASE_TYPE == 'mysql':
            return GenModelMySQLColumnType[typing].value
        else:
            if typing == 'CHARACTER VARYING':  # postgresql 中 DDL VARCHAR 的别名
                return 'str'
            return GenModelPostgreSQLColumnType[typing].value
    except KeyError:
        return 'str'
