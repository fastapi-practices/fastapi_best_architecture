#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from decimal import Decimal
from typing import Any, Sequence, TypeVar

import msgspec

from asgiref.sync import sync_to_async
from sqlalchemy import Row, RowMapping
from starlette.responses import JSONResponse

RowData = Row | RowMapping | Any

R = TypeVar('R', bound=RowData)


@sync_to_async
def select_columns_serialize(row: R) -> dict:
    """
    Serialize SQLAlchemy select table columns, does not contain relational columns

    :param row:
    :return:
    """
    obj_dict = {}
    for column in row.__table__.columns.keys():
        val = getattr(row, column)
        if isinstance(val, Decimal):
            if val % 1 == 0:
                val = int(val)
            val = float(val)
        obj_dict[column] = val
    return obj_dict


async def select_list_serialize(row: Sequence[R]) -> list:
    """
    Serialize SQLAlchemy select list

    :param row:
    :return:
    """
    ret_list = [await select_columns_serialize(_) for _ in row]
    return ret_list


@sync_to_async
def select_as_dict(row: R) -> dict:
    """
    Converting SQLAlchemy select to dict, which can contain relational data,
    depends on the properties of the select object itself

    :param row:
    :return:
    """
    obj_dict = row.__dict__
    if '_sa_instance_state' in obj_dict:
        del obj_dict['_sa_instance_state']
        return obj_dict


class MsgSpecJSONResponse(JSONResponse):
    """
    JSON response using the high-performance msgspec library to serialize data to JSON.
    """

    def render(self, content: Any) -> bytes:
        return msgspec.json.encode(content)
