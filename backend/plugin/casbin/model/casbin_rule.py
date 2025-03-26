#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import MappedBase, id_key


class CasbinRule(MappedBase):
    """Casbin 规则表"""

    __tablename__ = 'sys_casbin_rule'

    id: Mapped[id_key]
    ptype: Mapped[str] = mapped_column(String(255), comment='策略类型: p / g')
    v0: Mapped[str] = mapped_column(String(255), comment='用户 UUID / 角色 ID')
    v1: Mapped[str] = mapped_column(LONGTEXT().with_variant(TEXT, 'postgresql'), comment='API 路径 / 角色名称')
    v2: Mapped[str | None] = mapped_column(String(255), comment='请求方法')
    v3: Mapped[str | None] = mapped_column(String(255), comment='预留字段')
    v4: Mapped[str | None] = mapped_column(String(255), comment='预留字段')
    v5: Mapped[str | None] = mapped_column(String(255), comment='预留字段')

    def __str__(self) -> str:
        arr = [self.ptype]
        for v in (self.v0, self.v1, self.v2, self.v3, self.v4, self.v5):
            if v is None:
                break
            arr.append(v)
        return ', '.join(arr)

    def __repr__(self) -> str:
        return f'<CasbinRule {self.id}: "{str(self)}">'
