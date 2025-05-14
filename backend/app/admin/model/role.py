#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.admin.model.m2m import sys_role_data_scope, sys_role_menu, sys_user_role
from backend.common.model import Base, id_key

if TYPE_CHECKING:
    from backend.app.admin.model import DataScope, Menu, User


class Role(Base):
    """Rolesheet"""

    __tablename__ = 'sys_role'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(20), unique=True, comment='Role Name')
    status: Mapped[int] = mapped_column(default=1, comment='Role state (0 disabled 1)')
    remark: Mapped[str | None] = mapped_column(
        LONGTEXT().with_variant(TEXT, 'postgresql'), default=None, comment='Remarks'
    )

    # Role user pairs
    users: Mapped[list[User]] = relationship(init=False, secondary=sys_user_role, back_populates='roles')

    # Role menus are multiple
    menus: Mapped[list[Menu]] = relationship(init=False, secondary=sys_role_menu, back_populates='roles')

    # Role data range multiple to multiple
    scopes: Mapped[list[DataScope]] = relationship(init=False, secondary=sys_role_data_scope, back_populates='roles')
