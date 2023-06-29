#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import Field

from backend.app.common.enums import MenuType, StatusType
from backend.app.schemas.base import SchemaBase


class Meta(SchemaBase):
    roles: list[str] | None = None
    requiresAuth: bool = False
    icon: str | None = None
    locale: str | None = None
    hideInMenu: bool | None = None
    hideChildrenInMenu: bool | None = None
    activeMenu: str | None = None
    orderNo: int | None = None
    noAffix: bool | None = None
    ignoreCache: bool | None = None


class MenuBase(SchemaBase):
    name: str
    parent_id: int | None = Field(default=None, description='菜单父级ID')
    sort: int = Field(default=0, ge=0, description='排序')
    icon: str | None = None
    path: str | None = None
    menu_type: MenuType = Field(default=MenuType.directory, ge=0, description='菜单类型（0目录 1菜单 2按钮）')
    meta: Meta
    component: str | None = None
    perms: str | None = None
    status: StatusType = Field(default=StatusType.enable)
    remark: str | None = None


class CreateMenu(MenuBase):
    pass


class UpdateMenu(MenuBase):
    pass


class GetAllMenu(MenuBase):
    id: int
    created_time: datetime
    updated_time: datetime | None = None

    class Config:
        orm_mode = True
