#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.admin.model.m2m import sys_data_scope_rule
from backend.common.model import Base, id_key

if TYPE_CHECKING:
    from backend.app.admin.model import DataScope


class DataRule(Base):
    """数据规则表"""

    __tablename__ = 'sys_data_rule'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(500), unique=True, comment='名称')
    model: Mapped[str] = mapped_column(String(50), comment='SQLA 模型名，对应 DATA_PERMISSION_MODELS 键名')
    column: Mapped[str] = mapped_column(String(20), comment='模型字段名')
    operator: Mapped[int] = mapped_column(comment='运算符（0：and、1：or）')
    expression: Mapped[int] = mapped_column(
        comment='表达式（0：==、1：!=、2：>、3：>=、4：<、5：<=、6：in、7：not_in）'
    )
    value: Mapped[str] = mapped_column(String(255), comment='规则值')

    # 数据范围规则多对多
    scopes: Mapped[list[DataScope]] = relationship(init=False, secondary=sys_data_scope_rule, back_populates='rules')
