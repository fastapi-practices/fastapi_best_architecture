#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.enums import MethodType
from backend.common.schema import SchemaBase


class ApiSchemaBase(SchemaBase):
    """API 基础模型"""

    name: str = Field(description='API 名称')
    method: MethodType = Field(MethodType.GET, description='请求方法')
    path: str = Field(description='API 路径')
    remark: str | None = Field(None, description='备注')


class CreateApiParam(ApiSchemaBase):
    """创建 API 参数"""


class UpdateApiParam(ApiSchemaBase):
    """更新 API 参数"""


class GetApiDetail(ApiSchemaBase):
    """API 详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='API ID')
    created_time: datetime = Field(description='创建时间')
    updated_time: datetime | None = Field(None, description='更新时间')
