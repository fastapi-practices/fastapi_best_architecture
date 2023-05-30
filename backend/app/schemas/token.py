#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import BaseModel

from backend.app.schemas.user import GetUserInfoNoRelation


class SwaggerToken(BaseModel):
    access_token: str
    token_type: str = 'Bearer'
    user: GetUserInfoNoRelation


class AccessToken(BaseModel):
    access_token: str
    access_token_type: str = 'Bearer'
    access_token_expire_time: datetime


class LoginToken(AccessToken):
    refresh_token: str
    refresh_token_type: str = 'Bearer'
    refresh_token_expire_time: datetime
    user: GetUserInfoNoRelation


class RefreshToken(BaseModel):
    refresh_token: str
    refresh_token_type: str = 'Bearer'
    refresh_token_expire_time: datetime


class NewToken(AccessToken):
    pass
