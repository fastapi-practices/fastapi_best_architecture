#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict

from backend.common.schema import SchemaBase


class DataRuleSchemaBase(SchemaBase):
    name: str
    model: str
    column: str
    condition: str


class CreateDataRuleParam(DataRuleSchemaBase):
    pass


class UpdateDataRuleParam(DataRuleSchemaBase):
    pass


class GetDataRuleListDetails(DataRuleSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None
