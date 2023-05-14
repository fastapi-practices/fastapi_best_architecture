#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.base_class import Base, id_key
from backend.app.models.sys_role_menu import sys_role_menu


class Menu(Base):
    """菜单表"""

    __tablename__ = 'sys_menu'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(50), unique=True, comment='菜单名称')
    parent_id: Mapped[int] = mapped_column(default=0, comment='父菜单ID')
    level: Mapped[int] = mapped_column(default=0, comment='菜单层级')
    sort: Mapped[int] = mapped_column(default=0, comment='显示顺序')
    path: Mapped[str] = mapped_column(String(200), default='', comment='路由地址')
    menu_type: Mapped[int] = mapped_column(default=0, comment='菜单类型（0目录 1菜单 2按钮）')
    icon: Mapped[str | None] = mapped_column(String(100), default='#', comment='菜单图标')
    remark: Mapped[str | None] = mapped_column(LONGTEXT, default=None, comment='备注')
    del_flag: Mapped[bool] = mapped_column(default=True, comment='删除标志（0删除 1存在）')
    # 菜单角色多对多
    roles: Mapped[list['Role']] = relationship(  # noqa: F821
        init=False, secondary=sys_role_menu, back_populates='menus'
    )
