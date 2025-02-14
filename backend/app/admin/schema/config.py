#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict

from backend.common.schema import SchemaBase


class SaveBuiltInConfigParam(SchemaBase):
    name: str
    key: str
    value: str


class ConfigSchemaBase(SchemaBase):
    name: str
    type: str | None
    key: str
    value: str
    is_frontend: bool
    remark: str | None


class CreateConfigParam(ConfigSchemaBase):
    pass


class UpdateConfigParam(ConfigSchemaBase):
    pass


class GetConfigDetail(ConfigSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None
