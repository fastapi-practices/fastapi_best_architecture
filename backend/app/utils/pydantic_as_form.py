#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import Form


def encode_as_form(cls):
    """
    pydantic 类装饰器，将 pydantic 类转化为 form_data

    示例::

    @encode_as_form
    class Pydantic(BaseModel):
        ...

    :param cls:
    :return:
    """
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(default=Form(...))
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls
