#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import BaseModel, Field, validator

from backend.app.common.enums import MenuType


class MenuBase(BaseModel):
    menu_name: str
    parent_id: int = Field(default=0, ge=0, description='菜单父级ID')
    level: int = Field(default=0, ge=0, description='菜单层级')
    sort: int = Field(default=0, ge=0, description='排序')
    path: str = Field(..., description='路由地址')
    menu_type: int = Field(default=MenuType.directory, ge=0, description='菜单类型（0目录 1菜单 2按钮）')
    icon: str | None = None
    remark: str | None = None
    del_flag: bool

    @validator('menu_type')
    def check_menu_type(cls, v):
        if v not in MenuType.get_member_values():
            raise ValueError('菜单类型只能是0、1、2')
        return v


class CreateMenu(MenuBase):
    pass


class UpdateMenu(MenuBase):
    pass


class GetAllMenu(MenuBase):
    menu_id: int
    create_user: int
    update_user: int = None
    created_time: datetime
    updated_time: datetime | None = None

    class Config:
        orm_mode = True
