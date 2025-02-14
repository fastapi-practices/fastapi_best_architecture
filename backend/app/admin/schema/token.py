#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from backend.app.admin.schema.user import GetUserInfoNoRelationDetail
from backend.common.enums import StatusType
from backend.common.schema import SchemaBase


class GetSwaggerToken(SchemaBase):
    access_token: str
    token_type: str = 'Bearer'
    user: GetUserInfoNoRelationDetail


class AccessTokenBase(SchemaBase):
    access_token: str
    access_token_expire_time: datetime
    session_uuid: str


class GetNewToken(AccessTokenBase):
    pass


class GetLoginToken(AccessTokenBase):
    user: GetUserInfoNoRelationDetail


class KickOutToken(SchemaBase):
    session_uuid: str


class GetTokenDetail(SchemaBase):
    id: int
    session_uuid: str
    username: str
    nickname: str
    ip: str
    os: str
    browser: str
    device: str
    status: StatusType
    last_login_time: str
    expire_time: datetime
