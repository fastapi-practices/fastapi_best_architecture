#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import Field, validator

from backend.app.common.enums import StatusType
from backend.app.schemas.base import SchemaBase
from backend.app.utils.re_verify import is_phone


class DeptBase(SchemaBase):
    name: str
    parent_id: int | None = Field(default=None, description='菜单父级ID')
    sort: int = Field(default=0, ge=0, description='排序')
    leader: str | None = None
    phone: str | None = None
    email: str | None = None
    status: StatusType = Field(default=StatusType.enable)

    @validator('phone')
    def phone_validator(cls, v):
        if v is not None and not v.isdigit():
            if not is_phone(v):
                raise ValueError('手机号码输入有误')
        return v

    @validator('email')
    def email_validator(cls, v):
        if v is not None:
            from email_validator import EmailNotValidError, validate_email

            try:
                validate_email(v, check_deliverability=False).email
            except EmailNotValidError:
                raise ValueError('邮箱格式错误')
        return v


class CreateDept(DeptBase):
    pass


class UpdateDept(DeptBase):
    pass


class GetAllDept(DeptBase):
    id: int
    del_flag: bool
    created_time: datetime
    updated_time: datetime | None = None

    class Config:
        orm_mode = True
