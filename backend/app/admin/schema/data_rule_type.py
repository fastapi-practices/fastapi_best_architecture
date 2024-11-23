#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.enums import StatusType
from backend.common.schema import SchemaBase


class DataRuleTypeSchemaBase(SchemaBase):
    name: str
    status: StatusType = Field(default=StatusType.enable)
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
