#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydantic import Field

from backend.common.schema import SchemaBase


class RunParam(SchemaBase):
    name: str = Field(description='任务名称')
    args: list | None = Field(default=None, description='任务函数位置参数')
    kwargs: dict | None = Field(default=None, description='任务函数关键字参数')
