#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict

from backend.common.schema import SchemaBase


class DataRuleTypeSchemaBase(SchemaBase):
    name: str
    status: int
    remark: str


class CreateDataRuleTypeParam(DataRuleTypeSchemaBase):
    pass


class UpdateDataRuleTypeParam(DataRuleTypeSchemaBase):
    pass


class GetDataRuleTypeListDetails(DataRuleTypeSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None
