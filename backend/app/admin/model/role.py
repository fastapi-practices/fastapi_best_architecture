#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.admin.model.m2m import sys_role_data_rule, sys_role_menu, sys_user_role
from backend.common.model import Base, id_key


class Role(Base):
    """角色表"""

    __tablename__ = 'sys_role'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(20), unique=True, comment='角色名称')
    status: Mapped[int] = mapped_column(default=1, comment='角色状态（0停用 1正常）')
    remark: Mapped[str | None] = mapped_column(
        LONGTEXT().with_variant(TEXT, 'postgresql'), default=None, comment='备注'
    )

    # 角色用户多对多
    users: Mapped[list['User']] = relationship(init=False, secondary=sys_user_role, back_populates='roles')  # noqa: F821

    # 角色菜单多对多
    menus: Mapped[list['Menu']] = relationship(init=False, secondary=sys_role_menu, back_populates='roles')  # noqa: F821

    # 角色数据权限规则多对多
    rules: Mapped[list['DataRule']] = relationship(init=False, secondary=sys_role_data_rule, back_populates='roles')  # noqa: F821
