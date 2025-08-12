#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class GenBusinessSchemaBase(SchemaBase):
    """代码生成业务基础模型"""

    app_name: str = Field(description='应用名称（英文）')
    table_name: str = Field(description='表名称（英文）')
    doc_comment: str = Field(description='文档注释（用于函数/参数文档）')
    table_comment: str | None = Field(None, description='表描述')
    class_name: str | None = Field(None, description='用于 python 代码基础类名')
    schema_name: str | None = Field(None, description='用于 python Schema 代码基础类名')
    filename: str | None = Field(None, description='用于 python 代码基础文件名')
    default_datetime_column: bool = Field(True, description='是否存在默认时间列')
    api_version: str = Field('v1', description='代码生成 api 版本')
    gen_path: str | None = Field(None, description='代码生成路径')
    remark: str | None = Field(None, description='备注')


class CreateGenBusinessParam(GenBusinessSchemaBase):
    """创建代码生成业务参数"""


class UpdateGenBusinessParam(GenBusinessSchemaBase):
    """更新代码生成业务参数"""


class GetGenBusinessDetail(GenBusinessSchemaBase):
    """获取代码生成业务详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='主键 ID')
    created_time: datetime = Field(description='创建时间')
    updated_time: datetime | None = Field(None, description='更新时间')
