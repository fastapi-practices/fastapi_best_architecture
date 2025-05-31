#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.app.admin.schema.data_scope import GetDataScopeDetail
from backend.app.admin.schema.menu import GetMenuDetail
from backend.common.enums import StatusType
from backend.common.schema import SchemaBase


class RoleSchemaBase(SchemaBase):
    """角色基础模型"""

    name: str = Field(description='角色名称')
    status: StatusType = Field(StatusType.enable, description='状态')
    is_filter_scopes: bool = Field(True, description='过滤数据权限')
    remark: str | None = Field(None, description='备注')


class CreateRoleParam(RoleSchemaBase):
    """创建角色参数"""


class UpdateRoleParam(RoleSchemaBase):
    """更新角色参数"""


class UpdateRoleMenuParam(SchemaBase):
    """更新角色菜单参数"""

    menus: list[int] = Field(description='菜单 ID 列表')


class UpdateRoleScopeParam(SchemaBase):
    """更新角色数据范围参数"""

    scopes: list[int] = Field(description='数据范围 ID 列表')


class GetRoleDetail(RoleSchemaBase):
    """角色详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='角色 ID')
    created_time: datetime = Field(description='创建时间')
    updated_time: datetime | None = Field(None, description='更新时间')


class GetRoleWithRelationDetail(GetRoleDetail):
    """角色关联详情"""

    menus: list[GetMenuDetail | None] = Field([], description='菜单详情列表')
    scopes: list[GetDataScopeDetail | None] = Field([], description='数据范围列表')
