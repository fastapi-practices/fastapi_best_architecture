#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.enums import StatusType
from backend.common.schema import SchemaBase


class DictDataSchemaBase(SchemaBase):
    """字典数据基础模型"""

    type_id: int = Field(description='字典类型 ID')
    label: str = Field(description='字典标签')
    value: str = Field(description='字典值')
    sort: int = Field(description='排序')
    status: StatusType = Field(StatusType.enable, description='状态')
    remark: str | None = Field(None, description='备注')


class CreateDictDataParam(DictDataSchemaBase):
    """创建字典数据参数"""


class UpdateDictDataParam(DictDataSchemaBase):
    """更新字典数据参数"""


class DeleteDictDataParam(SchemaBase):
    """删除字典数据参数"""

    pks: list[int] = Field(description='字典数据 ID 列表')


class GetDictDataDetail(DictDataSchemaBase):
    """字典数据详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='字典数据 ID')
    type_code: str = Field(description='字典类型编码')
    created_time: datetime = Field(description='创建时间')
    updated_time: datetime | None = Field(None, description='更新时间')
