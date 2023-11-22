#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from email_validator import EmailNotValidError, validate_email
from pydantic import Field, HttpUrl, root_validator, validator

from backend.app.common.enums import StatusType
from backend.app.schemas.base import SchemaBase
from backend.app.schemas.dept import GetAllDept
from backend.app.schemas.role import GetAllRole


class Auth(SchemaBase):
    username: str
    password: str


class AuthLogin(Auth):
    captcha: str


class RegisterUser(Auth):
    nickname: str | None = None
    email: str = Field(..., example='user@example.com')

    @validator('email')
    def email_validate(cls, v):
        try:
            validate_email(v, check_deliverability=False).email
        except EmailNotValidError:
            raise ValueError('邮箱格式错误')
        return v


class AddUser(Auth):
    dept_id: int
    roles: list[int]
    nickname: str | None = None
    email: str = Field(..., example='user@example.com')

    @validator('email')
    def email_validate(cls, v):
        try:
            validate_email(v, check_deliverability=False).email
        except EmailNotValidError:
            raise ValueError('邮箱格式错误')
        return v


class _UserInfoBase(SchemaBase):
    dept_id: int | None = None
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
    pass


class UpdateUserRole(SchemaBase):
    roles: list[int]


class Avatar(SchemaBase):
    url: HttpUrl = Field(..., description='头像 http 地址')


class GetUserInfoNoRelation(_UserInfoBase):
    dept_id: int | None = None
    id: int
    uuid: str
    avatar: str | None = None
    status: StatusType = Field(default=StatusType.enable)
    is_superuser: bool
    is_staff: bool
    is_multi_login: bool
    join_time: datetime = None
    last_login_time: datetime | None = None

    class Config:
        orm_mode = True


class GetAllUserInfo(GetUserInfoNoRelation):
    dept: GetAllDept | None = None
    roles: list[GetAllRole]

    class Config:
        orm_mode = True


class GetCurrentUserInfo(GetAllUserInfo):
    @root_validator
    def handel(cls, values):
        """处理部门和角色"""
        dept = values.get('dept')
        if dept:
            values['dept'] = dept.name
        roles = values.get('roles')
        if roles:
            values['roles'] = [role.name for role in roles]
        return values

    class Config:
        orm_mode = True


class ResetPassword(SchemaBase):
    old_password: str
    new_password: str
    confirm_password: str
