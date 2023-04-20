#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class Auth(BaseModel):
    username: str
    password: str


class CreateUser(Auth):
    email: str = Field(..., example='user@example.com')


class UpdateUser(BaseModel):
    username: str
    email: str
    mobile_number: Optional[str] = None


class Avatar(BaseModel):
    url: HttpUrl = Field(..., description='头像地址')


class GetUserInfo(UpdateUser):
    id: int
    uid: str
    avatar: Optional[str] = None
    time_joined: datetime.datetime = None
    last_login: Optional[datetime.datetime] = None
    is_superuser: bool
    is_active: bool

    class Config:
        orm_mode = True


class ResetPassword(BaseModel):
    id: int = Field(..., example='1', description='用户ID')
    password1: str
    password2: str
