#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl


class Auth(BaseModel):
    username: str
    password: str


class CreateUser(Auth):
    email: str = Field(..., example='user@example.com')


class UpdateUser(BaseModel):
    username: str
    email: str
    mobile_number: str | None = None


class Avatar(BaseModel):
    url: HttpUrl = Field(..., description='头像地址')


class GetUserInfo(UpdateUser):
    id: int
    uid: str
    avatar: str | None = None
    is_active: bool
    is_superuser: bool
    time_joined: datetime = None
    last_login: datetime | None = None

    class Config:
        orm_mode = True


class ResetPassword(BaseModel):
    id: int = Field(..., example='1', description='用户ID')
    password1: str
    password2: str
