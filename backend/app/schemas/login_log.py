#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import BaseModel


class LoginLogBase(BaseModel):
    user_uuid: str
    username: str
    status: bool
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
    id: int
    create_time: datetime

    class Config:
        orm_mode = True
