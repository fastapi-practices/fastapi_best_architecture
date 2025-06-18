#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.enums import RoleDataRuleExpressionType, RoleDataRuleOperatorType
from backend.common.schema import SchemaBase


class DataRuleSchemaBase(SchemaBase):
    """数据规则基础模型"""

    name: str = Field(description='规则名称')
    model: str = Field(description='模型名称')
    column: str = Field(description='字段名称')
    operator: RoleDataRuleOperatorType = Field(RoleDataRuleOperatorType.AND, description='操作符（AND/OR）')
    expression: RoleDataRuleExpressionType = Field(RoleDataRuleExpressionType.eq, description='表达式类型')
    value: str = Field(description='规则值')


class CreateDataRuleParam(DataRuleSchemaBase):
    """创建数据规则参数"""


class UpdateDataRuleParam(DataRuleSchemaBase):
    """更新数据规则参数"""


class DeleteDataRuleParam(SchemaBase):
    """删除数据规则参数"""

    pks: list[int] = Field(description='规则 ID 列表')


class GetDataRuleDetail(DataRuleSchemaBase):
    """数据规则详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='规则 ID')
    created_time: datetime = Field(description='创建时间')
    updated_time: datetime | None = Field(None, description='更新时间')


class GetDataRuleColumnDetail(SchemaBase):
    """数据规则可用模型字段详情"""

    key: str = Field(description='字段名')
    comment: str = Field(description='字段评论')
