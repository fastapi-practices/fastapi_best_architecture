#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.admin.model.m2m import sys_role_data_rule
from backend.common.model import Base, id_key


class DataRule(Base):
    """数据权限规则表"""

    __tablename__ = 'sys_data_rule'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(255), unique=True, comment='规则名称')
    model: Mapped[str] = mapped_column(String(50), comment='SQLA 模型类')
    column: Mapped[str] = mapped_column(String(20), comment='数据库字段')
    operator: Mapped[int] = mapped_column(comment='运算符（0：and、1：or）')
    expression: Mapped[int] = mapped_column(
        comment='表达式（0：==、1：!=、2：>、3：>=、4：<、5：<=、6：in、7：not_in）'
    )
    value: Mapped[str] = mapped_column(String(255), comment='规则值')

    # 角色规则多对多
    roles: Mapped[list['Role']] = relationship(init=False, secondary=sys_role_data_rule, back_populates='rules')  # noqa: F821
