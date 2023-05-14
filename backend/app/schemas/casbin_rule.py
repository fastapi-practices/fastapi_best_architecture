#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from curses.ascii import isupper

from pydantic import BaseModel, Field, validator

from backend.app.common.enums import MethodType


class RBACBase(BaseModel):
    sub: str = Field(..., description='用户uuid / 角色')


class CreatePolicy(RBACBase):
    path: str = Field(..., description='api路径')
    method: str = Field(default=MethodType.GET, description='请求方法')

    @validator('method')
    def check_method(cls, v):
        if not isupper(v):
            raise ValueError('请求方式必须大写')
        allow_method = MethodType.get_member_values()
        if v not in allow_method:
            raise ValueError(f'请求方式不合法, 仅支持: {allow_method}')
        return v


class UpdatePolicy(CreatePolicy):
    pass


class DeletePolicy(CreatePolicy):
    pass


class UserRole(BaseModel):
    uuid: str = Field(..., description='用户uuid')
    role: str = Field(..., description='角色')


class GetAllPolicy(BaseModel):
    id: int
    ptype: str
    v0: str
    v1: str
    v2: str | None = None
    v3: str | None = None
    v4: str | None = None
    v5: str | None = None

    class Config:
        orm_mode = True
