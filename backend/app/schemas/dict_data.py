#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import BaseModel

from backend.app.schemas.dict_type import GetAllDictType


class DictDataBase(BaseModel):
    label: str
    value: str
    sort: int
    status: bool
    remark: str | None = None
    type_id: int


class CreateDictData(DictDataBase):
    pass


class UpdateDictData(DictDataBase):
    pass


class GetAllDictData(DictDataBase):
    id: int
    type: GetAllDictType
    create_user: int
    update_user: int = None
    created_time: datetime
    updated_time: datetime | None = None

    class Config:
        orm_mode = True
