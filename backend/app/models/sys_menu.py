#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Union

from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.base_class import Base, id_key
from backend.app.models.sys_role_menu import sys_role_menu


class Menu(Base):
    """菜单表"""

    __tablename__ = 'sys_menu'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(50), unique=True, comment='菜单名称')
    level: Mapped[int] = mapped_column(default=0, comment='菜单层级')
    sort: Mapped[int] = mapped_column(default=0, comment='排序')
    icon: Mapped[str | None] = mapped_column(String(100), default=None, comment='菜单图标')
    path: Mapped[str | None] = mapped_column(String(200), default=None, comment='路由地址')
    menu_type: Mapped[int] = mapped_column(default=0, comment='菜单类型（0目录 1菜单 2按钮）')
    component: Mapped[str | None] = mapped_column(String(255), default=None, comment='组件路径')
    perms: Mapped[str | None] = mapped_column(String(100), default=None, comment='权限标识')
    status: Mapped[int] = mapped_column(default=1, comment='菜单状态（0停用 1正常）')
    remark: Mapped[str | None] = mapped_column(LONGTEXT, default=None, comment='备注')
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey('sys_menu.id', ondelete='SET NULL'), default=None, index=True, comment='父菜单ID'
    )
    # 父级菜单一对多
    parent: Mapped[Union['Menu', None]] = relationship(init=False, back_populates='children', remote_side=[id])
    children: Mapped[list['Menu'] | None] = relationship(init=False, back_populates='parent')
    # 菜单角色多对多
    roles: Mapped[list['Role']] = relationship(  # noqa: F821
        init=False, secondary=sys_role_menu, back_populates='menus'
    )
