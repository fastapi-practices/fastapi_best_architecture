#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.enums import StatusType
from backend.common.schema import SchemaBase


class DictTypeSchemaBase(SchemaBase):
    name: str
    code: str
    status: StatusType = Field(default=StatusType.enable)
    remark: str | None = None


class CreateDictTypeParam(DictTypeSchemaBase):
    pass


class UpdateDictTypeParam(DictTypeSchemaBase):
    pass


class GetDictTypeListDetails(DictTypeSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None
