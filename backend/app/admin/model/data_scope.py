#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.admin.model.m2m import sys_data_scope_rule, sys_role_data_scope
from backend.common.model import Base, id_key

if TYPE_CHECKING:
    from backend.app.admin.model import DataRule, Role


class DataScope(Base):
    """数据范围表"""

    __tablename__ = 'sys_data_scope'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(50), unique=True, comment='名称')
    status: Mapped[int] = mapped_column(default=1, comment='状态（0停用 1正常）')

    # 数据范围规则多对多
    rules: Mapped[list[DataRule]] = relationship(init=False, secondary=sys_data_scope_rule, back_populates='scopes')

    # 角色数据范围多对多
    roles: Mapped[list[Role]] = relationship(init=False, secondary=sys_role_data_scope, back_populates='scopes')
