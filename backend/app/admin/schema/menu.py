#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.enums import MenuType, StatusType
from backend.common.schema import SchemaBase


class MenuSchemaBase(SchemaBase):
    """菜单基础模型"""

    title: str = Field(description='菜单标题')
    name: str = Field(description='菜单名称')
    path: str = Field(description='路由路径')
    parent_id: int | None = Field(None, description='菜单父级 ID')
    sort: int = Field(0, ge=0, description='排序')
    icon: str | None = Field(None, description='图标')
    type: MenuType = Field(MenuType.directory, description='菜单类型（0目录 1菜单 2按钮）')
    component: str | None = Field(None, description='组件路径')
    perms: str | None = Field(None, description='权限标识')
    status: StatusType = Field(StatusType.enable, description='状态')
    display: StatusType = Field(StatusType.enable, description='是否显示')
    cache: StatusType = Field(StatusType.enable, description='是否缓存')
    link: str | None = Field(None, description='外链地址')
    remark: str | None = Field(None, description='备注')


class CreateMenuParam(MenuSchemaBase):
    """创建菜单参数"""


class UpdateMenuParam(MenuSchemaBase):
    """更新菜单参数"""


class GetMenuDetail(MenuSchemaBase):
    """菜单详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='菜单 ID')
    created_time: datetime = Field(description='创建时间')
    updated_time: datetime | None = Field(None, description='更新时间')
