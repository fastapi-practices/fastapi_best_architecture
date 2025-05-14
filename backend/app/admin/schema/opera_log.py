#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Any

from pydantic import ConfigDict, Field

from backend.common.enums import StatusType
from backend.common.schema import SchemaBase


class OperaLogSchemaBase(SchemaBase):
    """Operation log base model"""

    trace_id: str = Field(description='TRACK ID')
    username: str | None = Field(None, description='Username')
    method: str = Field(description='Method of request')
    title: str = Field(description='Operation Title')
    path: str = Field(description='Request Path')
    ip: str = Field(description='IP ADDRESS')
    country: str | None = Field(None, description='Country')
    region: str | None = Field(None, description='Region')
    city: str | None = Field(None, description='Urban')
    user_agent: str = Field(description='User-Agent')
    os: str | None = Field(None, description='Operating systems')
    browser: str | None = Field(None, description='Browser')
    device: str | None = Field(None, description='Equipment')
    args: dict[str, Any] | None = Field(None, description='Request parameters')
    status: StatusType = Field(StatusType.enable, description='Status')
    code: str = Field(description='Status Code')
    msg: str | None = Field(None, description='Message')
    cost_time: float = Field(description='Time-consuming')
    opera_time: datetime = Field(description='Operation Time')


class CreateOperaLogParam(OperaLogSchemaBase):
    """Create operational log parameters"""


class UpdateOperaLogParam(OperaLogSchemaBase):
    """Update operational log parameters"""


class GetOperaLogDetail(OperaLogSchemaBase):
    """Operations log details"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='LOG ID')
    created_time: datetime = Field(description='Created')
