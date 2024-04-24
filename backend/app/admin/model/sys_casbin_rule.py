#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import MappedBase, id_key


class CasbinRule(MappedBase):
    """重写 casbin 中的 CasbinRule model 类, 使用自定义 Base, 避免产生 alembic 迁移问题"""

    __tablename__ = 'sys_casbin_rule'

    id: Mapped[id_key]
    ptype: Mapped[str] = mapped_column(String(255), comment='策略类型: p / g')
    v0: Mapped[str] = mapped_column(String(255), comment='角色ID / 用户uuid')
    v1: Mapped[str] = mapped_column(LONGTEXT, comment='api路径 / 角色名称')
    v2: Mapped[str | None] = mapped_column(String(255), comment='请求方法')
    v3: Mapped[str | None] = mapped_column(String(255))
    v4: Mapped[str | None] = mapped_column(String(255))
    v5: Mapped[str | None] = mapped_column(String(255))

    def __str__(self):
        arr = [self.ptype]
        for v in (self.v0, self.v1, self.v2, self.v3, self.v4, self.v5):
            if v is None:
                break
            arr.append(v)
        return ', '.join(arr)

    def __repr__(self):
        return '<CasbinRule {}: "{}">'.format(self.id, str(self))
