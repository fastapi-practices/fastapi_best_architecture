#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from curses.ascii import isupper
from datetime import datetime

from pydantic import BaseModel, Field, validator

from backend.app.common.enums import MethodType


class ApiBase(BaseModel):
    name: str
    method: str = Field(default=MethodType.GET, description='请求方法')
    path: str = Field(..., description='api路径')
    remark: str | None = None

    @validator('method')
    def check_method(cls, v):
        if not isupper(v):
            raise ValueError('请求方式必须大写')
        allow_method = MethodType.get_member_values()
        if v not in allow_method:
            raise ValueError(f'请求方式不合法, 仅支持: {allow_method}')
        return v


class CreateApi(ApiBase):
    pass


class UpdateApi(ApiBase):
    pass


class GetAllApi(ApiBase):
    id: int
    create_user: int
    update_user: int = None
    created_time: datetime
    updated_time: datetime | None = None

    class Config:
        orm_mode = True
