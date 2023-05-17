#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import BaseModel, Field


class DeptBase(BaseModel):
    name: str
    parent_id: int = Field(default=0, ge=0, description='菜单父级ID')
    level: int = Field(default=0, ge=0, description='菜单层级')
    sort: int = Field(default=0, ge=0, description='排序')
    leader: str | None = None
    phone: str | None = None
    email: str | None = None
    status: bool
    del_flag: bool


class CreateDept(DeptBase):
    pass


class UpdateDept(DeptBase):
    pass


class GetAllDept(DeptBase):
    id: int
    create_user: int
    update_user: int = None
    created_time: datetime
    updated_time: datetime | None = None

    class Config:
        orm_mode = True
