#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import BaseModel, Field, validator

from backend.app.schemas.user import GetUserInfoNoRelation


class SwaggerToken(BaseModel):
    access_token: str
    token_type: str = 'Bearer'
    user: GetUserInfoNoRelation


class LoginToken(BaseModel):
    access_token: str
    access_token_type: str = 'Bearer'
    access_token_expire_time: datetime
    refresh_token: str
    refresh_token_type: str = 'Bearer'
    refresh_token_expire_time: datetime
    user: GetUserInfoNoRelation


class RefreshToken(BaseModel):
    refresh_token: str
    refresh_token_type: str = 'Bearer'
    refresh_token_expire_time: datetime


class RefreshTokenTime(BaseModel):
    expire_time: datetime | None = Field(None, description='自定义刷新令牌过期时间')

    @validator('expire_time', pre=True)
    def validate_expire_time(cls, v):
        if v is None:
            return None
        if not isinstance(v, str) or 'T' not in v:
            raise ValueError('输入时间格式错误')
        v = datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%fZ')
        if v < datetime.now():
            raise ValueError('输入时间不能小于当前时间')
        return v
