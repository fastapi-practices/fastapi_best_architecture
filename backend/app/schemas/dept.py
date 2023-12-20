#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, EmailStr, Field

from backend.app.common.enums import StatusType
from backend.app.schemas.base import CustomPhoneNumber, SchemaBase


class DeptBase(SchemaBase):
    name: str
    parent_id: int | None = Field(default=None, description='菜单父级ID')
    sort: int = Field(default=0, ge=0, description='排序')
    leader: str | None = None
    phone: CustomPhoneNumber | None = None
    email: EmailStr | None = None
    status: StatusType = Field(default=StatusType.enable)


class CreateDept(DeptBase):
    pass


class UpdateDept(DeptBase):
    pass


class GetAllDept(DeptBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    del_flag: bool
    created_time: datetime
    updated_time: datetime | None = None
