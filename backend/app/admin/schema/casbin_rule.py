#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydantic import ConfigDict, Field

from backend.common.enums import MethodType
from backend.common.schema import SchemaBase


class CreatePolicyParam(SchemaBase):
    sub: str = Field(..., description='用户uuid / 角色ID')
    path: str = Field(..., description='api 路径')
    method: MethodType = Field(default=MethodType.GET, description='请求方法')


class UpdatePolicyParam(CreatePolicyParam):
    pass


class DeletePolicyParam(CreatePolicyParam):
    pass


class DeleteAllPoliciesParam(SchemaBase):
    uuid: str | None = None
    role: str


class CreateUserRoleParam(SchemaBase):
    uuid: str = Field(..., description='用户 uuid')
    role: str = Field(..., description='角色')


class DeleteUserRoleParam(CreateUserRoleParam):
    pass


class GetPolicyListDetails(SchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ptype: str = Field(..., description='规则类型, p / g')
    v0: str = Field(..., description='用户 uuid / 角色')
    v1: str = Field(..., description='api 路径 / 角色')
    v2: str | None = None
    v3: str | None = None
    v4: str | None = None
    v5: str | None = None
