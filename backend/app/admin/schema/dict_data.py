#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.app.admin.schema.dict_type import GetDictTypeListDetails
from backend.common.enums import StatusType
from backend.common.schema import SchemaBase


class DictDataSchemaBase(SchemaBase):
    type_id: int
    label: str
    value: str
    sort: int
    status: StatusType = Field(default=StatusType.enable)
    remark: str | None = None


class CreateDictDataParam(DictDataSchemaBase):
    pass


class UpdateDictDataParam(DictDataSchemaBase):
    pass


class GetDictDataListDetails(DictDataSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    type: GetDictTypeListDetails
    created_time: datetime
    updated_time: datetime | None = None
