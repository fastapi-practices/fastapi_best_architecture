#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.app.common.enums import StatusType
from backend.app.schemas.base import SchemaBase


class DictTypeBase(SchemaBase):
    name: str
    code: str
    status: StatusType = Field(default=StatusType.enable)
    remark: str | None = None


class CreateDictType(DictTypeBase):
    pass


class UpdateDictType(DictTypeBase):
    pass


class GetAllDictType(DictTypeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None
