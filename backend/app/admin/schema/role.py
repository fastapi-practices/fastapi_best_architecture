#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.app.admin.schema.menu import GetMenuListDetails
from backend.common.enums import RoleDataScopeType, StatusType
from backend.common.schema import SchemaBase


class RoleSchemaBase(SchemaBase):
    name: str
    status: StatusType = Field(default=StatusType.enable)
    remark: str | None = None


class CreateRoleParam(RoleSchemaBase):
    pass


class UpdateRoleParam(RoleSchemaBase):
    pass


class UpdateRoleMenuParam(SchemaBase):
    menus: list[int]


class UpdateRoleDataScopeParam(SchemaBase):
    data_scope: RoleDataScopeType = Field(
        default=RoleDataScopeType.all,
        description='数据权限范围（0: 全部数据，1: 自定义数据，2: 所在部门及以下数据，3: 所在部门数据，4: 仅本人数据）',
    )


class UpdateRoleDeptParam(SchemaBase):
    depts: list[int]


class GetRoleListDetails(RoleSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None
    menus: list[GetMenuListDetails]
