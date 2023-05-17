#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import BaseModel, HttpUrl, Field

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


class _UserInfoBase(BaseModel):
    dept_id: int
    username: str
    nickname: str
    email: str = Field(..., example='user@example.com')
    phone: str | None = None


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
    time_joined: datetime = None
    last_login: datetime | None = None

    class Config:
        orm_mode = True


class GetUserInfo(GetUserInfoNoRelation):
    dept: GetAllDept | None = None
    roles: list[GetAllRole]

    class Config:
        orm_mode = True


class ResetPassword(BaseModel):
    id: int
    password1: str
    password2: str
