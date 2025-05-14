#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class SaveBuiltInConfigParam(SchemaBase):
    """Save built-in parameters configuration parameters"""

    name: str = Field(description='Parameter Configuration Name')
    key: str = Field(description='Parameter Configuration Keyname')
    value: str = Field(description='Parameter Configuration Values')


class ConfigSchemaBase(SchemaBase):
    """Parameter Configuration Base Model"""

    name: str = Field(description='Parameter Configuration Name')
    type: str | None = Field(None, description='Parameter Configuration Type')
    key: str = Field(description='Parameter Configuration Keyname')
    value: str = Field(description='Parameter Configuration Values')
    is_frontend: bool = Field(description='Whether to configure front-end parameters')
    remark: str | None = Field(None, description='Remarks')


class CreateConfigParam(ConfigSchemaBase):
    """Create Parameter Configuration Parameters"""


class UpdateConfigParam(ConfigSchemaBase):
    """Update parameter configuration parameters"""


class GetConfigDetail(ConfigSchemaBase):
    """Parameter Configuration Details"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='PARAMETER CONFIGURATION ID')
    created_time: datetime = Field(description='Created')
    updated_time: datetime | None = Field(None, description='Update Time')
