#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import BaseModel, Field, validator

from backend.app.common.enums import RoleDataScope, StatusType
from backend.app.schemas.menu import GetAllMenu


class RoleBase(BaseModel):
    name: str
    data_scope: RoleDataScope = Field(default=RoleDataScope.custom, description='数据范围（1：全部数据权限 2：自定数据权限）')  # noqa: E501
    status: StatusType = Field(default=StatusType.enable)
    remark: str | None = None

    @validator('data_scope')
    def data_scope_validator(cls, v):
        if v not in RoleDataScope.get_member_values():
            raise ValueError('数据范围只能是 1 或 2')
        return v


class CreateRole(RoleBase):
    menus: list[int]


class UpdateRole(RoleBase):
    menus: list[int]


class GetAllRole(RoleBase):
    id: int
    create_user: int
    update_user: int = None
    created_time: datetime
    updated_time: datetime | None = None
    menus: list[GetAllMenu]

    class Config:
        orm_mode = True
