#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.common.model import Base, id_key

if TYPE_CHECKING:
    from backend.plugin.data_permission.model import DataScope


class DataRule(Base):
    """数据规则表"""

    __tablename__ = 'sys_data_rule'

    id: Mapped[id_key] = mapped_column(init=False)
    model: Mapped[str] = mapped_column(String(50), comment='SQLA 模型类名')
    column: Mapped[str] = mapped_column(String(20), comment='模型字段名')
    operator: Mapped[int] = mapped_column(comment='运算符（0：and、1：or）')
    expression: Mapped[int] = mapped_column(
        comment='表达式（0：==、1：!=、2：>、3：>=、4：<、5：<=、6：in、7：not_in）'
    )
    value: Mapped[str] = mapped_column(String(255), comment='规则值')
    remark: Mapped[str] = mapped_column(
        LONGTEXT().with_variant(TEXT, 'postgresql'), comment='备注'
    )

    # 数据范围规则一对多
    rule_id: Mapped[int | None] = mapped_column(ForeignKey('sys_data_scope.id', ondelete='SET NULL'),
                                                default=None,comment='数据范围关联 ID')
    rule: Mapped[DataScope] = relationship(init=False, back_populates='rules')


