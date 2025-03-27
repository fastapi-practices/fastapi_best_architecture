#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.enums import StatusType
from backend.common.schema import SchemaBase


class DictTypeSchemaBase(SchemaBase):
    """字典类型基础模型"""

    name: str = Field(description='字典名称')
    code: str = Field(description='字典编码')
    status: StatusType = Field(StatusType.enable, description='状态')
    remark: str | None = Field(None, description='备注')


class CreateDictTypeParam(DictTypeSchemaBase):
    """创建字典类型参数"""


class UpdateDictTypeParam(DictTypeSchemaBase):
    """更新字典类型参数"""


class GetDictTypeDetail(DictTypeSchemaBase):
    """字典类型详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='字典类型 ID')
    created_time: datetime = Field(description='创建时间')
    updated_time: datetime | None = Field(None, description='更新时间')
