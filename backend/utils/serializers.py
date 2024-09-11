#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from decimal import Decimal
from typing import Any, Sequence, TypeVar

from fastapi.encoders import decimal_encoder
from msgspec import json
from sqlalchemy import Row, RowMapping
from sqlalchemy.orm import ColumnProperty, SynonymProperty, class_mapper
from starlette.responses import JSONResponse

RowData = Row | RowMapping | Any

R = TypeVar('R', bound=RowData)


def select_columns_serialize(row: R) -> dict:
    """
    Serialize SQLAlchemy select table columns, does not contain relational columns

    :param row:
    :return:
    """
    result = {}
    for column in row.__table__.columns.keys():
        v = getattr(row, column)
        if isinstance(v, Decimal):
            v = decimal_encoder(v)
        result[column] = v
    return result


def select_list_serialize(row: Sequence[R]) -> list:
    """
    Serialize SQLAlchemy select list

    :param row:
    :return:
    """
    result = [select_columns_serialize(_) for _ in row]
    return result


def select_as_dict(row: R, use_alias: bool = False) -> dict:
    """
    Converting SQLAlchemy select to dict, which can contain relational data,
    depends on the properties of the select object itself

    If set use_alias is True, the column name will be returned as alias,
    If alias doesn't exist in columns, we don't recommend setting it to True

    :param row:
    :param use_alias:
    :return:
    """
    if not use_alias:
        result = row.__dict__
        if '_sa_instance_state' in result:
            del result['_sa_instance_state']
            return result
    else:
        result = {}
        mapper = class_mapper(row.__class__)
        for prop in mapper.iterate_properties:
            if isinstance(prop, (ColumnProperty, SynonymProperty)):
                key = prop.key
                result[key] = getattr(row, key)
        return result


class MsgSpecJSONResponse(JSONResponse):
    """
    JSON response using the high-performance msgspec library to serialize data to JSON.
    """

    def render(self, content: Any) -> bytes:
        return json.encode(content)
