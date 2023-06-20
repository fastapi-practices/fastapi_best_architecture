#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import Field, validator

from backend.app.common.enums import MethodType
from backend.app.schemas.base import SchemaBase


class ApiBase(SchemaBase):
    name: str
    method: MethodType = Field(default=MethodType.GET, description='请求方法')
    path: str = Field(..., description='api路径')
    remark: str | None = None

    @validator('method')
    def method_validator(cls, v):
        if not v.isupper():
            raise ValueError('请求方式必须大写')
        return v


class CreateApi(ApiBase):
    pass


class UpdateApi(ApiBase):
    pass


class GetAllApi(ApiBase):
    id: int
    created_time: datetime
    updated_time: datetime | None = None

    class Config:
        orm_mode = True
