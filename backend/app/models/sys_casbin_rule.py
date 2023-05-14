#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database.base_class import id_key, MappedBase


class CasbinRule(MappedBase):
    """
    重写 casbin_sqlalchemy_adapter 中的 casbinRule model类, 使用自定义 MappedBase, 避免产生 alembic 迁移问题
    """
    __tablename__ = 'sys_casbin_rule'

    id: Mapped[id_key]
    ptype: Mapped[str] = mapped_column(String(255), comment='策略类型: p 或者 g')
    v0: Mapped[str] = mapped_column(String(255), comment='角色 / 用户uuid')
    v1: Mapped[str] = mapped_column(LONGTEXT, comment='api路径 / 角色名称')
    v2: Mapped[str | None] = mapped_column(String(255), comment='请求方法')
    v3: Mapped[str | None] = mapped_column(String(255))
    v4: Mapped[str | None] = mapped_column(String(255))
    v5: Mapped[str | None] = mapped_column(String(255))
