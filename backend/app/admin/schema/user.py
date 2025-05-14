#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Any

from pydantic import ConfigDict, EmailStr, Field, HttpUrl, model_validator
from typing_extensions import Self

from backend.app.admin.schema.dept import GetDeptDetail
from backend.app.admin.schema.role import GetRoleWithRelationDetail
from backend.common.enums import StatusType
from backend.common.schema import CustomPhoneNumber, SchemaBase


class AuthSchemaBase(SchemaBase):
    """User Authentication Base Model"""

    username: str = Field(description='Username')
    password: str | None = Field(description='Password')


class AuthLoginParam(AuthSchemaBase):
    """User login parameters"""

    captcha: str = Field(description='Authentication Code')


class RegisterUserParam(AuthSchemaBase):
    """User registration parameters"""

    nickname: str | None = Field(None, description='Nickname')
    email: EmailStr = Field(examples=['user@example.com'], description='Mailbox')


class AddUserParam(AuthSchemaBase):
    """Add user parameters"""

    dept_id: int = Field(description='SECTOR ID')
    roles: list[int] = Field(description='ROLE ID LIST')
    nickname: str | None = Field(None, description='Nickname')
    email: EmailStr = Field(examples=['user@example.com'], description='Mailbox')


class ResetPasswordParam(SchemaBase):
    """Reset password parameters"""

    old_password: str = Field(description='Old password')
    new_password: str = Field(description='New Password')
    confirm_password: str = Field(description='Confirm password')


class UserInfoSchemaBase(SchemaBase):
    """User information base model"""

    dept_id: int | None = Field(None, description='SECTOR ID')
    username: str = Field(description='Username')
    nickname: str = Field(description='Nickname')
    email: EmailStr = Field(examples=['user@example.com'], description='Mailbox')
    phone: CustomPhoneNumber | None = Field(None, description='Cell phone number')


class UpdateUserParam(UserInfoSchemaBase):
    """Update user parameters"""


class UpdateUserRoleParam(SchemaBase):
    """Update user role parameters"""

    roles: list[int] = Field(description='ROLE ID LIST')


class AvatarParam(SchemaBase):
    """Update header parameters"""

    url: HttpUrl = Field(description='image http address')


class GetUserInfoDetail(UserInfoSchemaBase):
    """User Info Details"""

    model_config = ConfigDict(from_attributes=True)

    dept_id: int | None = Field(None, description='SECTOR ID')
    id: int = Field(description='USER ID')
    uuid: str = Field(description='USER UUID')
    avatar: str | None = Field(None, description='Heads')
    status: StatusType = Field(StatusType.enable, description='Status')
    is_superuser: bool = Field(description='Whether Super Administrator')
    is_staff: bool = Field(description='Whether to administrate')
    is_multi_login: bool = Field(description='Whether multiple login is allowed')
    join_time: datetime = Field(description='Organisation')
    last_login_time: datetime | None = Field(None, description='Last Login Time')


class GetUserInfoWithRelationDetail(GetUserInfoDetail):
    """User information contact details"""

    model_config = ConfigDict(from_attributes=True)

    dept: GetDeptDetail | None = Field(None, description='Sectoral information')
    roles: list[GetRoleWithRelationDetail] = Field(description='Role List')


class GetCurrentUserInfoWithRelationDetail(GetUserInfoWithRelationDetail):
    """Current user information contact details"""

    model_config = ConfigDict(from_attributes=True)

    dept: str | None = Field(None, description='Department name')
    roles: list[str] = Field(description='Role Name List')

    @model_validator(mode='before')
    @classmethod
    def handel(cls, data: Any) -> Self:
        """Processing sector and role data"""
        dept = data['dept']
        if dept:
            data['dept'] = dept['name']
        roles = data['roles']
        if roles:
            data['roles'] = [role['name'] for role in roles]
        return data
