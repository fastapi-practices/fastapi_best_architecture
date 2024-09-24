#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.common.enums import GenModelMySQLColumnType


def sql_type_to_sqlalchemy(typing: str) -> str:
    """
    Converts a sql type to a SQLAlchemy type.

    :param typing:
    :return:
    """
    if typing in GenModelMySQLColumnType.get_member_keys():
        return typing
    return 'String'


def sql_type_to_pydantic(typing: str) -> str:
    """
    Converts a sql type to a pydantic type.

    :param typing:
    :return:
    """
    try:
        return GenModelMySQLColumnType[typing].value
    except KeyError:
        return 'str'
