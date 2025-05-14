#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.enums import StatusType
from backend.common.schema import SchemaBase


class DictTypeSchemaBase(SchemaBase):
    """Dictionary Type Base Model"""

    name: str = Field(description='Dictionary Name')
    code: str = Field(description='Dictionary encoding')
    status: StatusType = Field(StatusType.enable, description='Status')
    remark: str | None = Field(None, description='Remarks')


class CreateDictTypeParam(DictTypeSchemaBase):
    """Create dictionary type parameters"""


class UpdateDictTypeParam(DictTypeSchemaBase):
    """Update dictionary type parameters"""


class GetDictTypeDetail(DictTypeSchemaBase):
    """Dictionary type details"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='DICTIONARY TYPE ID')
    created_time: datetime = Field(description='Created')
    updated_time: datetime | None = Field(None, description='Update Time')
