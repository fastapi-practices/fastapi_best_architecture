#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.admin.model.sys_role_menu import sys_role_menu
from backend.app.admin.model.sys_user_role import sys_user_role
from backend.common.model import Base, id_key


class Role(Base):
    """角色表"""

    __tablename__ = 'sys_role'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(20), unique=True, comment='角色名称')
    data_scope: Mapped[int | None] = mapped_column(default=2, comment='权限范围（1：全部数据权限 2：自定义数据权限）')
    status: Mapped[int] = mapped_column(default=1, comment='角色状态（0停用 1正常）')
    remark: Mapped[str | None] = mapped_column(LONGTEXT, default=None, comment='备注')
    # 角色用户多对多
    users: Mapped[list['User']] = relationship(  # noqa: F821
        init=False, secondary=sys_user_role, back_populates='roles'
    )
    # 角色菜单多对多
    menus: Mapped[list['Menu']] = relationship(  # noqa: F821
        init=False, secondary=sys_role_menu, back_populates='roles'
    )
