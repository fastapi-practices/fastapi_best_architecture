#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class SaveBuiltInConfigParam(SchemaBase):
    """保存内置配置参数"""

    name: str = Field(description='配置名称')
    key: str = Field(description='配置键名')
    value: str = Field(description='配置值')


class ConfigSchemaBase(SchemaBase):
    """配置基础模型"""

    name: str = Field(description='配置名称')
    type: str | None = Field(default=None, description='配置类型')
    key: str = Field(description='配置键名')
    value: str = Field(description='配置值')
    is_frontend: bool = Field(description='是否前端配置')
    remark: str | None = Field(default=None, description='备注')


class CreateConfigParam(ConfigSchemaBase):
    """创建配置参数"""


class UpdateConfigParam(ConfigSchemaBase):
    """更新配置参数"""


class GetConfigDetail(ConfigSchemaBase):
    """配置详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='配置 ID')
    created_time: datetime = Field(description='创建时间')
    updated_time: datetime | None = Field(default=None, description='更新时间')
