#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.enums import MenuType, StatusType
from backend.common.schema import SchemaBase


class MenuSchemaBase(SchemaBase):
    """Menu Foundation Model"""

    title: str = Field(description='Menu Title')
    name: str = Field(description='Menu Name')
    path: str = Field(description='Route Path')
    parent_id: int | None = Field(None, description='MENU PARENT ID')
    sort: int = Field(0, ge=0, description='Sort')
    icon: str | None = Field(None, description='Icon')
    type: MenuType = Field(MenuType.directory, description='Menu type (0 directory 1 menu 2 button)')
    component: str | None = Field(None, description='Component Path')
    perms: str | None = Field(None, description='Permission Identification')
    status: StatusType = Field(StatusType.enable, description='Status')
    display: StatusType = Field(StatusType.enable, description='Whether to show')
    cache: StatusType = Field(StatusType.enable, description='Cache')
    link: str | None = Field(None, description='Outlink Address')
    remark: str | None = Field(None, description='Remarks')


class CreateMenuParam(MenuSchemaBase):
    """Create menu parameters"""


class UpdateMenuParam(MenuSchemaBase):
    """Update menu parameters"""


class GetMenuDetail(MenuSchemaBase):
    """Menu Details"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='MENU ID')
    created_time: datetime = Field(description='Created')
    updated_time: datetime | None = Field(None, description='Update Time')
