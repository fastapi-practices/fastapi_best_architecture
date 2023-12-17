#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict

from backend.app.schemas.base import SchemaBase


class LoginLogBase(SchemaBase):
    user_uuid: str
    username: str
    status: int
    ip: str
    country: str | None
    region: str | None
    city: str | None
    user_agent: str
    browser: str | None
    os: str | None
    device: str | None
    msg: str
    login_time: datetime


class CreateLoginLog(LoginLogBase):
    pass


class UpdateLoginLog(LoginLogBase):
    pass


class GetAllLoginLog(LoginLogBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
