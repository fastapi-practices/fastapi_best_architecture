#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key


class Config(Base):
    """系统配置表"""

    __tablename__ = 'sys_config'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(20), comment='名称')
    type: Mapped[str] = mapped_column(String(20), comment='类型')
    key: Mapped[str] = mapped_column(String(50), comment='键名')
    value: Mapped[str] = mapped_column(LONGTEXT, comment='键值')
