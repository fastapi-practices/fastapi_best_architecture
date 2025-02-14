#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Any

from pydantic import ConfigDict, EmailStr, Field, HttpUrl, model_validator
from typing_extensions import Self

from backend.app.admin.schema.dept import GetDeptDetail
from backend.app.admin.schema.role import GetRoleDetail
from backend.common.enums import StatusType
from backend.common.schema import CustomPhoneNumber, SchemaBase


class AuthSchemaBase(SchemaBase):
    username: str
    password: str | None


class AuthLoginParam(AuthSchemaBase):
    captcha: str


class RegisterUserParam(AuthSchemaBase):
    nickname: str | None = None
    email: EmailStr = Field(examples=['user@example.com'])


class AddUserParam(AuthSchemaBase):
    dept_id: int
    roles: list[int]
    nickname: str | None = None
    email: EmailStr = Field(examples=['user@example.com'])


class UserInfoSchemaBase(SchemaBase):
    dept_id: int | None = None
    username: str
    nickname: str
    email: EmailStr = Field(examples=['user@example.com'])
    phone: CustomPhoneNumber | None = None


class UpdateUserParam(UserInfoSchemaBase):
    pass


class UpdateUserRoleParam(SchemaBase):
    roles: list[int]


class AvatarParam(SchemaBase):
    url: HttpUrl = Field(description='头像 http 地址')


class GetUserInfoNoRelationDetail(UserInfoSchemaBase):
    model_config = ConfigDict(from_attributes=True)

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


class GetUserInfoDetail(GetUserInfoNoRelationDetail):
    model_config = ConfigDict(from_attributes=True)

    dept: GetDeptDetail | None = None
    roles: list[GetRoleDetail]


class GetCurrentUserInfoDetail(GetUserInfoDetail):
    model_config = ConfigDict(from_attributes=True)

    dept: str | None = None
    roles: list[str]

    @model_validator(mode='before')
    @classmethod
    def handel(cls, data: Any) -> Self:
        """处理部门和角色"""
        dept = data['dept']
        if dept:
            data['dept'] = dept['name']
        roles = data['roles']
        if roles:
            data['roles'] = [role['name'] for role in roles]
        return data


class CurrentUserIns(GetUserInfoDetail):
    model_config = ConfigDict(from_attributes=True)


class ResetPasswordParam(SchemaBase):
    old_password: str
    new_password: str
    confirm_password: str
