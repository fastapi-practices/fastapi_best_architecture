#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydantic import ConfigDict, Field, field_validator

from backend.app.common.enums import MethodType
from backend.app.schemas.base import SchemaBase


class CreatePolicy(SchemaBase):
    sub: str = Field(..., description='用户uuid / 角色ID')
    path: str = Field(..., description='api 路径')
    method: MethodType = Field(default=MethodType.GET, description='请求方法')

    @field_validator('method')
    @classmethod
    def method_validator(cls, v):
        if not v.isupper():
            raise ValueError('请求方式必须大写')
        return v


class UpdatePolicy(CreatePolicy):
    pass


class DeletePolicy(CreatePolicy):
    pass


class DeleteAllPolicies(SchemaBase):
    uuid: str | None = None
    role: str


class CreateUserRole(SchemaBase):
    uuid: str = Field(..., description='用户 uuid')
    role: str = Field(..., description='角色')


class DeleteUserRole(CreateUserRole):
    pass


class GetAllPolicy(SchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ptype: str = Field(..., description='规则类型, p / g')
    v0: str = Field(..., description='用户 uuid / 角色')
    v1: str = Field(..., description='api 路径 / 角色')
    v2: str | None = None
    v3: str | None = None
    v4: str | None = None
    v5: str | None = None
