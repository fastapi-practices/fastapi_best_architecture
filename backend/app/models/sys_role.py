#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.base_class import Base, id_key
from backend.app.models.sys_role_menu import sys_role_menu
from backend.app.models.sys_user_role import sys_user_role


class Role(Base):
    """角色表"""

    __tablename__ = 'sys_role'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(20), unique=True, comment='角色名称')
    sort: Mapped[int] = mapped_column(default=0, comment='显示顺序')
    data_scope: Mapped[int | None] = mapped_column(default=2, comment='数据范围（1：全部数据权限 2：自定数据权限）')
    del_flag: Mapped[bool] = mapped_column(default=True, comment='删除标志（0删除 1存在）')
    # 角色用户多对多
    users: Mapped[list['User']] = relationship(  # noqa: F821
        init=False, secondary=sys_user_role, back_populates='roles'
    )
    # 角色菜单多对多
    menus: Mapped[list['Menu']] = relationship(  # noqa: F821
        init=False, secondary=sys_role_menu, back_populates='roles'
    )
