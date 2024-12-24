#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Boolean, String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.dialects.postgresql import INTEGER, TEXT
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key


class Config(Base):
    """系统配置表"""

    __tablename__ = 'sys_config'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(20), comment='名称')
    type: Mapped[str | None] = mapped_column(String(20), server_default=None, comment='类型')
    key: Mapped[str] = mapped_column(String(50), unique=True, comment='键名')
    value: Mapped[str] = mapped_column(LONGTEXT().with_variant(TEXT, 'postgresql'), comment='键值')
    is_frontend: Mapped[bool] = mapped_column(
        Boolean().with_variant(INTEGER, 'postgresql'), default=False, comment='是否前端'
    )
    remark: Mapped[str | None] = mapped_column(
        LONGTEXT().with_variant(TEXT, 'postgresql'), default=None, comment='备注'
    )
