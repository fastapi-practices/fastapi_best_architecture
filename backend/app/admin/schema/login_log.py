#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class LoginLogSchemaBase(SchemaBase):
    """Login Logging Foundation Model"""

    user_uuid: str = Field(description='USER UUID')
    username: str = Field(description='Username')
    status: int = Field(description='Login Status')
    ip: str = Field(description='IP ADDRESS')
    country: str | None = Field(None, description='Country')
    region: str | None = Field(None, description='Region')
    city: str | None = Field(None, description='Urban')
    user_agent: str = Field(description='User-Agent')
    browser: str | None = Field(None, description='Browser')
    os: str | None = Field(None, description='Operating systems')
    device: str | None = Field(None, description='Equipment')
    msg: str = Field(description='Message')
    login_time: datetime = Field(description='Login Time')


class CreateLoginLogParam(LoginLogSchemaBase):
    """Create login parameters"""


class UpdateLoginLogParam(LoginLogSchemaBase):
    """Update log login parameters"""


class GetLoginLogDetail(LoginLogSchemaBase):
    """Login Login Details"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='LOG ID')
    created_time: datetime = Field(description='Created')
