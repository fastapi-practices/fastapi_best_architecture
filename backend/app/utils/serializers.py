#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from decimal import Decimal
from typing import Any, TypeVar, Sequence

from sqlalchemy import Row, RowMapping

RowData = Row | RowMapping | Any

R = TypeVar('R', bound=RowData)


def select_to_dict(row: R) -> dict:
    """
    Serialize SQLAlchemy Select to dict

    :param row:
    :return:
    """
    obj_dict = {}
    for column in row.__table__.columns.keys():
        val = getattr(row, column)
        if isinstance(val, Decimal):
            val = float(val)
        obj_dict[column] = val
    return obj_dict


def select_to_list(row: Sequence[R]) -> list:
    """
    Serialize SQLAlchemy Select to list

    :param row:
    :return:
    """
    ret_list = [select_to_dict(_) for _ in row]
    return ret_list


def select_to_json(row: R) -> dict:
    """
    Serialize SQLAlchemy Select to json

    :param row:
    :return:
    """
    obj_dict = row.__dict__
    if '_sa_instance_state' in obj_dict:
        del obj_dict['_sa_instance_state']
        return obj_dict
