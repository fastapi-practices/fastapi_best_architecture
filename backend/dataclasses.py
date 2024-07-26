#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import dataclasses

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
