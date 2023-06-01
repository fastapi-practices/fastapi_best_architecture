#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import BaseModel


class LoginLogBase(BaseModel):
    user_uuid: str
    username: str
    status: bool
    ipaddr: str
    location: str
    browser: str
    os: str
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
