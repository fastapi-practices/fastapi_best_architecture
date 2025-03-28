#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydantic import ConfigDict, Field

from backend.common.enums import MethodType
from backend.common.schema import SchemaBase


class CreatePolicyParam(SchemaBase):
    """创建 P 策略参数"""

    sub: str = Field(description='用户 UUID / 角色 ID')
    path: str = Field(description='API 路径')
    method: MethodType = Field(MethodType.GET, description='请求方法')


class UpdatePolicyParam(SchemaBase):
    """更新 P 策略参数"""

    old: CreatePolicyParam = Field(description='原策略')
    new: CreatePolicyParam = Field(description='新策略')


class UpdatePoliciesParam(SchemaBase):
    """批量更新策略参数"""

    old: list[CreatePolicyParam] = Field(description='原策略列表')
    new: list[CreatePolicyParam] = Field(description='新策略列表')


class DeletePolicyParam(CreatePolicyParam):
    """删除策略参数"""


class DeleteAllPoliciesParam(SchemaBase):
    """删除所有策略参数"""

    uuid: str | None = Field(None, description='用户 UUID')
    role: str = Field(description='角色')


class CreateGroupParam(SchemaBase):
    """创建 G 策略参数"""

    uuid: str = Field(description='用户 UUID')
    role: str = Field(description='角色')


class DeleteGroupParam(CreateGroupParam):
    """删除 G 策略参数"""


class GetPolicyDetail(SchemaBase):
    """策略详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='规则 ID')
    ptype: str = Field(description='规则类型, p / g')
    v0: str = Field(description='用户 UUID / 角色 ID')
    v1: str = Field(description='API 路径 / 角色')
    v2: str | None = Field(None, description='请求方法')
    v3: str | None = Field(None, description='预留字段')
    v4: str | None = Field(None, description='预留字段')
    v5: str | None = Field(None, description='预留字段')
