#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.app.common.enums import StatusType
from backend.app.schemas.base import SchemaBase


class OperaLogBase(SchemaBase):
    username: str | None = None
    method: str
    title: str
    path: str
    ip: str
    country: str | None = None
    region: str | None = None
    city: str | None = None
    user_agent: str
    os: str | None = None
    browser: str | None = None
    device: str | None = None
    args: dict | None = None
    status: StatusType = Field(default=StatusType.enable)
    code: str
    msg: str | None = None
    cost_time: float
    opera_time: datetime


class CreateOperaLog(OperaLogBase):
    pass


class UpdateOperaLog(OperaLogBase):
    pass


class GetAllOperaLog(OperaLogBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
