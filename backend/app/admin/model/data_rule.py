#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key


class DataRule(Base):
    """数据权限规则表"""

    __tablename__ = 'data_rule'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(255), comment='规则名称')
    model: Mapped[str] = mapped_column(String(50), comment='SQLA 模型类')
    column: Mapped[str] = mapped_column(String(20), comment='数据库字段')
    condition: Mapped[str] = mapped_column(String(20), comment='查询条件')
