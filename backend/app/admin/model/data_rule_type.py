#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key


class DataRuleType(Base):
    """数据权限规则类型表"""

    __tablename__ = 'data_rule_type'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(255), comment='规则类型名')
    status: Mapped[int] = mapped_column(default=1, comment='状态（0停用 1正常）')
    remark: Mapped[str | None] = mapped_column(LONGTEXT, default=None, comment='备注')
