#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.enums import StatusType
from backend.common.schema import SchemaBase
from backend.plugin.dict.schema.dict_type import GetDictTypeDetail


class DictDataSchemaBase(SchemaBase):
    """Dictionary Data Base Model"""

    type_id: int = Field(description='DICTIONARY TYPE ID')
    label: str = Field(description='Dictionary Label')
    value: str = Field(description='Dictionary values')
    sort: int = Field(description='Sort')
    status: StatusType = Field(StatusType.enable, description='Status')
    remark: str | None = Field(None, description='Remarks')


class CreateDictDataParam(DictDataSchemaBase):
    """Create dictionary data parameters"""


class UpdateDictDataParam(DictDataSchemaBase):
    """Update dictionary data parameters"""


class GetDictDataDetail(DictDataSchemaBase):
    """Dictionary data details"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='DICTIONARY DATA ID')
    created_time: datetime = Field(description='Created')
    updated_time: datetime | None = Field(None, description='Update Time')


class GetDictDataWithRelation(DictDataSchemaBase):
    """Dictionary data association details"""

    type: GetDictTypeDetail | None = Field(None, description='Dictionary Type Information')
