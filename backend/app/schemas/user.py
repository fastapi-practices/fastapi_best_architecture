#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from email_validator import validate_email, EmailNotValidError
from pydantic import BaseModel, HttpUrl, Field, validator

from backend.app.schemas.dept import GetAllDept
from backend.app.schemas.role import GetAllRole


class Auth(BaseModel):
    username: str
    password: str


class CreateUser(Auth):
    dept_id: int
    roles: list[int]
    nickname: str
    email: str = Field(..., example='user@example.com')

    @validator('email')
    def email_validate(cls, v):
        try:
            validate_email(v, check_deliverability=False).email
        except EmailNotValidError:
            raise ValueError('邮箱格式错误')
        return v


class _UserInfoBase(BaseModel):
    dept_id: int
    username: str
    nickname: str
    email: str = Field(..., example='user@example.com')
    phone: str | None = None

    @validator('email')
    def email_validate(cls, v):
        try:
            validate_email(v, check_deliverability=False).email
        except EmailNotValidError:
            raise ValueError('邮箱格式错误')
        return v

    @validator('phone')
    def phone_validate(cls, v):
        if v is not None and not v.isdigit():
            raise ValueError('手机号格式错误')
        return v


class UpdateUser(_UserInfoBase):
    roles: list[int]


class Avatar(BaseModel):
    url: HttpUrl = Field(..., description='头像 http 地址')


class GetUserInfoNoRelation(_UserInfoBase):
    id: int
    user_uuid: str
    avatar: str | None = None
    is_active: bool
    is_superuser: bool
    is_multi_login: bool
    time_joined: datetime = None
    last_login: datetime | None = None

    class Config:
        orm_mode = True


class GetAllUserInfo(GetUserInfoNoRelation):
    dept_id: int | None = None
    dept: GetAllDept | None = None
    roles: list[GetAllRole]

    class Config:
        orm_mode = True


class ResetPassword(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str
