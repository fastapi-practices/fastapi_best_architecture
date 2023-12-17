#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.app.common.enums import RoleDataScopeType, StatusType
from backend.app.schemas.base import SchemaBase
from backend.app.schemas.menu import GetAllMenu


class RoleBase(SchemaBase):
    name: str
    data_scope: RoleDataScopeType = Field(
        default=RoleDataScopeType.custom, description='权限范围（1：全部数据权限 2：自定义数据权限）'
    )
    status: StatusType = Field(default=StatusType.enable)
    remark: str | None = None


class CreateRole(RoleBase):
    pass


class UpdateRole(RoleBase):
    pass


class UpdateRoleMenu(SchemaBase):
    menus: list[int]


class GetAllRole(RoleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None
    menus: list[GetAllMenu]
