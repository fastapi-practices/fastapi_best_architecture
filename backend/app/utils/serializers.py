#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from decimal import Decimal

from sqlalchemy.sql import Select


def select_to_dict(obj: Select) -> dict:
    """
    Serialize SQLAlchemy Select to dict

    :param obj:
    :return:
    """
    obj_dict = {}
    for column in obj.__table__.columns.keys():
        val = getattr(obj, column)
        if isinstance(val, Decimal):
            val = float(val)
        obj_dict[column] = val
    return obj_dict


def select_to_list(obj: list) -> list:
    """
    Serialize SQLAlchemy Select to list

    :param obj:
    :return:
    """
    ret_list = []
    for _ in obj:
        ret_dict = select_to_dict(_)
        ret_list.append(ret_dict)
    return ret_list


def select_to_json(obj: Select) -> dict:
    """
    Serialize SQLAlchemy Select to json

    :param obj:
    :return:
    """
    obj_dict = obj.__dict__
    if '_sa_instance_state' in obj_dict:
        del obj_dict['_sa_instance_state']
        return obj_dict
