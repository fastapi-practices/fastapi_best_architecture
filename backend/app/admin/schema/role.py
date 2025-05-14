#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.app.admin.schema.data_scope import GetDataScopeDetail
from backend.app.admin.schema.menu import GetMenuDetail
from backend.common.enums import StatusType
from backend.common.schema import SchemaBase


class RoleSchemaBase(SchemaBase):
    """Role Foundation Model"""

    name: str = Field(description='Role Name')
    status: StatusType = Field(StatusType.enable, description='Status')
    remark: str | None = Field(None, description='Remarks')


class CreateRoleParam(RoleSchemaBase):
    """Create role parameters"""


class UpdateRoleParam(RoleSchemaBase):
    """Update role parameters"""


class UpdateRoleMenuParam(SchemaBase):
    """Update Role Menu Parameter"""

    menus: list[int] = Field(description='MENU ID LIST')


class UpdateRoleScopeParam(SchemaBase):
    """Update role data range parameters"""

    scopes: list[int] = Field(description='DATA RANGE ID LIST')


class GetRoleDetail(RoleSchemaBase):
    """Role Details"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='ROLE ID')
    created_time: datetime = Field(description='Created')
    updated_time: datetime | None = Field(None, description='Update Time')


class GetRoleWithRelationDetail(GetRoleDetail):
    """Role Link Details"""

    menus: list[GetMenuDetail | None] = Field([], description='Menu Details List')
    scopes: list[GetDataScopeDetail | None] = Field([], description='Data Range List')
