#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field, field_validator

from backend.app.common.enums import MethodType
from backend.app.schemas.base import SchemaBase


class ApiBase(SchemaBase):
    name: str
    method: MethodType = Field(default=MethodType.GET, description='请求方法')
    path: str = Field(..., description='api路径')
    remark: str | None = None

    @field_validator('method')
    @classmethod
    def method_validator(cls, v):
        if not v.isupper():
            raise ValueError('请求方式必须大写')
        return v


class CreateApi(ApiBase):
    pass


class UpdateApi(ApiBase):
    pass


class GetAllApi(ApiBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None
