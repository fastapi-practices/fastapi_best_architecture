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


def select_columns_serialize(row: R) -> dict[str, Any]:
    """
    Columns of SQLAlchemy query table, excluding associated columns

    :param row: SQLAlchemy query result line
    :return:
    """
    result = {}
    for column in row.__table__.columns.keys():
        value = getattr(row, column)
        if isinstance(value, Decimal):
            value = decimal_encoder(value)
        result[column] = value
    return result


def select_list_serialize(row: Sequence[R]) -> list[dict[str, Any]]:
    """
    Sequenced SQLAlchemy Query List

    :param row: SQLAlchemy query list
    :return:
    """
    return [select_columns_serialize(item) for item in row]


def select_as_dict(row: R, use_alias: bool = False) -> dict[str, Any]:
    """
    Convert SQLAlchemy query results to a dictionary that contains associated data

    :param row: SQLAlchemy query result line
    :param use_alias: whether to use aliases for listing
    :return:
    """
    if not use_alias:
        result = row.__dict__
        if '_sa_instance_state' in result:
            del result['_sa_instance_state']
    else:
        result = {}
        mapper = class_mapper(row.__class__)  # type: ignore
        for prop in mapper.iterate_properties:
            if isinstance(prop, (ColumnProperty, SynonymProperty)):
                key = prop.key
                result[key] = getattr(row, key)

    return result


class MsgSpecJSONResponse(JSONResponse):
    """
    Use high performance msgspec library to sequence data into the JSON response class
    """

    def render(self, content: Any) -> bytes:
        return json.encode(content)
