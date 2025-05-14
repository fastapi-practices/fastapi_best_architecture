#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.common.model import Base, id_key

if TYPE_CHECKING:
    from backend.app.admin.model import DataScope


class DataRule(Base):
    """Data rule sheet"""

    __tablename__ = 'sys_data_rule'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(500), unique=True, comment='Name')
    model: Mapped[str] = mapped_column(String(50), comment='SQLA MODEL NAME, CORRESPONDING TO DATA_PERMISSION_MODES')
    column: Mapped[str] = mapped_column(String(20), comment='Model field name')
    operator: Mapped[int] = mapped_column(comment='operators (0:and, 1:or)')
    expression: Mapped[int] = mapped_column(
        comment='expressions (0: =, 1:! =, 2:>, 3:>, 4:<, 5:: < , 6:in, 7:not_in)'
    )
    value: Mapped[str] = mapped_column(String(255), comment='Rule value')

    # Data range rules are multiple
    scope_id: Mapped[int | None] = mapped_column(
        ForeignKey('sys_data_scope.id', ondelete='SET NULL'), default=None, comment='DATA RANGE CORRELATION ID'
    )
    scope: Mapped[DataScope] = relationship(init=False, back_populates='rules')
