#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydantic import ConfigDict, Field, field_validator

from backend.common.schema import SchemaBase
from backend.plugin.code_generator.utils.type_conversion import sql_type_to_sqlalchemy


class GenModelSchemaBase(SchemaBase):
    """代码生成模型基础模型"""

    name: str = Field(description='列名称')
    comment: str | None = Field(None, description='列描述')
    type: str = Field(description='SQLA 模型列类型')
    default: str | None = Field(None, description='列默认值')
    sort: int = Field(description='列排序')
    length: int = Field(description='列长度')
    is_pk: bool = Field(False, description='是否主键')
    is_nullable: bool = Field(False, description='是否可为空')
    gen_business_id: int = Field(description='代码生成业务ID')

    @field_validator('type')
    @classmethod
    def type_update(cls, v: str) -> str:
        """更新列类型"""
        return sql_type_to_sqlalchemy(v)


class CreateGenModelParam(GenModelSchemaBase):
    """创建代码生成模型参数"""


class UpdateGenModelParam(GenModelSchemaBase):
    """更新代码生成模型参数"""


class GetGenModelDetail(GenModelSchemaBase):
    """获取代码生成模型详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='主键 ID')
    pd_type: str = Field(description='列类型对应的 pydantic 类型')
