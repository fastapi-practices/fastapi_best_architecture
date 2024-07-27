#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import dataclasses

from datetime import datetime

from fastapi import Response

from backend.common.enums import StatusType


@dataclasses.dataclass
class IpInfo:
    ip: str
    country: str | None
    region: str | None
    city: str | None


@dataclasses.dataclass
class UserAgentInfo:
    user_agent: str
    os: str | None
    browser: str | None
    device: str | None


@dataclasses.dataclass
class RequestCallNextReturn:
    code: str
    msg: str
    status: StatusType
    err: Exception | None
    response: Response


@dataclasses.dataclass
class NewTokenReturn:
    new_access_token: str
    new_refresh_token: str
    new_access_token_expire_time: datetime
    new_refresh_token_expire_time: datetime
