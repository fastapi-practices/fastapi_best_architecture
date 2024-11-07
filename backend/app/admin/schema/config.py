#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict

from backend.common.enums import ConfigType
from backend.common.schema import SchemaBase


class ConfigSchemaBase(SchemaBase):
    name: str
    type: ConfigType = ConfigType.website
    key: str
    value: str


class CreateConfigParam(ConfigSchemaBase):
    pass


class UpdateConfigParam(ConfigSchemaBase):
    pass


class GetConfigListDetails(ConfigSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None
