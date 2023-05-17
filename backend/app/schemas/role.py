#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import BaseModel, Field, validator

from backend.app.common.enums import RoleDataScope
from backend.app.schemas.menu import GetAllMenu


class RoleBase(BaseModel):
    name: str
    sort: int = Field(default=0, ge=0, description='排序')
    data_scope: int | None = Field(default=RoleDataScope.custom, description='数据范围（1：全部数据权限 2：自定数据权限）')  # noqa: E501
    del_flag: bool

    @validator('data_scope')
    def check_data_scope(cls, v):
        if v not in RoleDataScope.get_member_values():
            raise ValueError('数据范围只能是1或2')
        return v


class CreateRole(RoleBase):
    menu_ids: list[int]


class UpdateRole(RoleBase):
    menu_ids: list[int]


class GetAllRole(RoleBase):
    id: int
    create_user: int
    update_user: int = None
    created_time: datetime
    updated_time: datetime | None = None
    menus: list[GetAllMenu]

    class Config:
        orm_mode = True
