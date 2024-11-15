#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydantic import Field

from backend.common.schema import SchemaBase


class ImportParam(SchemaBase):
    app: str = Field(description='应用名称，用于代码生成到指定 app')
    table_name: str = Field(description='数据库表名')
    table_schema: str = Field(description='数据库名')
