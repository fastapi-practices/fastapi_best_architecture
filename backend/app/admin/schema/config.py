#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict

from backend.common.schema import SchemaBase


class ConfigSchemaBase(SchemaBase):
    name: str
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


class AnyConfigSchemaBase(ConfigSchemaBase):
    type: str | None
    is_frontend: bool
    remark: str


class CreateAnyConfigParam(AnyConfigSchemaBase):
    pass


class UpdateAnyConfigParam(AnyConfigSchemaBase):
    pass


class GetAnyConfigListDetails(AnyConfigSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None
