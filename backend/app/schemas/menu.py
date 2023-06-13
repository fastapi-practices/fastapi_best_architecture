#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import BaseModel, Field, validator

from backend.app.common.enums import MenuType


class MenuBase(BaseModel):
    name: str
    parent_id: int = Field(default=None, ge=1, description='菜单父级ID')
    sort: int = Field(default=0, ge=0, description='排序')
    icon: str | None = None
    path: str | None = None
    menu_type: int = Field(default=MenuType.directory, ge=0, description='菜单类型（0目录 1菜单 2按钮）')
    component: str | None = None
    perms: str | None = None
    status: bool
    remark: str | None = None

    @validator('menu_type')
    def menu_type_validator(cls, v):
        if v not in MenuType.get_member_values():
            raise ValueError('菜单类型只能是 0，1，2')
        return v


class CreateMenu(MenuBase):
    pass


class UpdateMenu(MenuBase):
    pass


class GetAllMenu(MenuBase):
    id: int
    create_user: int
    update_user: int = None
    created_time: datetime
    updated_time: datetime | None = None

    class Config:
        orm_mode = True
