#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Union

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.admin.model.sys_role_menu import sys_role_menu
from backend.common.model import Base, id_key


class Menu(Base):
    """菜单表"""

    __tablename__ = 'sys_menu'

    id: Mapped[id_key] = mapped_column(init=False)
    title: Mapped[str] = mapped_column(String(50), comment='菜单标题')
    name: Mapped[str] = mapped_column(String(50), comment='菜单名称')
    level: Mapped[int] = mapped_column(default=0, comment='菜单层级')
    sort: Mapped[int] = mapped_column(default=0, comment='排序')
    icon: Mapped[str | None] = mapped_column(String(100), default=None, comment='菜单图标')
    path: Mapped[str | None] = mapped_column(String(200), default=None, comment='路由地址')
    menu_type: Mapped[int] = mapped_column(default=0, comment='菜单类型（0目录 1菜单 2按钮）')
    component: Mapped[str | None] = mapped_column(String(255), default=None, comment='组件路径')
    perms: Mapped[str | None] = mapped_column(String(100), default=None, comment='权限标识')
    status: Mapped[int] = mapped_column(default=1, comment='菜单状态（0停用 1正常）')
    show: Mapped[int] = mapped_column(default=1, comment='是否显示（0否 1是）')
    cache: Mapped[int] = mapped_column(default=1, comment='是否缓存（0否 1是）')
    remark: Mapped[str | None] = mapped_column(LONGTEXT, default=None, comment='备注')
    # 父级菜单一对多
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey('sys_menu.id', ondelete='SET NULL'), default=None, index=True, comment='父菜单ID'
    )
    parent: Mapped[Union['Menu', None]] = relationship(init=False, back_populates='children', remote_side=[id])
    children: Mapped[list['Menu'] | None] = relationship(init=False, back_populates='parent')
    # 菜单角色多对多
    roles: Mapped[list['Role']] = relationship(  # noqa: F821
        init=False, secondary=sys_role_menu, back_populates='menus'
    )
