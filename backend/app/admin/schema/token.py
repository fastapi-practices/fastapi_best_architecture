#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import Field

from backend.app.admin.schema.user import GetUserInfoDetail
from backend.common.enums import StatusType
from backend.common.schema import SchemaBase


class GetSwaggerToken(SchemaBase):
    """Swagger authentication token"""

    access_token: str = Field(description='Access tokens')
    token_type: str = Field('Bearer', description='token type')
    user: GetUserInfoDetail = Field(description='User Information')


class AccessTokenBase(SchemaBase):
    """Access token base model"""

    access_token: str = Field(description='Access tokens')
    access_token_expire_time: datetime = Field(description='Validity of tokens')
    session_uuid: str = Field(description='SESSION UUID')


class GetNewToken(AccessTokenBase):
    """Get a new token"""


class GetLoginToken(AccessTokenBase):
    """Fetch Login tokens"""

    user: GetUserInfoDetail = Field(description='User Information')


class KickOutToken(SchemaBase):
    """Kick the token"""

    session_uuid: str = Field(description='SESSION UUID')


class GetTokenDetail(SchemaBase):
    """token details"""

    id: int = Field(description='USER ID')
    session_uuid: str = Field(description='SESSION UUID')
    username: str = Field(description='Username')
    nickname: str = Field(description='Nickname')
    ip: str = Field(description='IP ADDRESS')
    os: str = Field(description='Operating systems')
    browser: str = Field(description='Browser')
    device: str = Field(description='Equipment')
    status: StatusType = Field(description='Status')
    last_login_time: str = Field(description='Last Login Time')
    expire_time: datetime = Field(description='Expiry Time')
