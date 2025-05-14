#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.admin.model.m2m import sys_role_data_scope
from backend.common.model import Base, id_key

if TYPE_CHECKING:
    from backend.app.admin.model import DataRule, Role


class DataScope(Base):
    """Data Range Table"""

    __tablename__ = 'sys_data_scope'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(50), unique=True, comment='Name')
    status: Mapped[int] = mapped_column(default=1, comment='Status (0 disabled 1)')

    # Data range rules are multiple
    rules: Mapped[list[DataRule]] = relationship(init=False, back_populates='scope')

    # Role data range multiple to multiple
    roles: Mapped[list[Role]] = relationship(init=False, secondary=sys_role_data_scope, back_populates='scopes')
