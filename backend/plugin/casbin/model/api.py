#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key


class Api(Base):
    """系统api"""

    __tablename__ = 'sys_api'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(50), unique=True, comment='api名称')
    method: Mapped[str] = mapped_column(String(16), comment='请求方法')
    path: Mapped[str] = mapped_column(String(500), comment='api路径')
    remark: Mapped[str | None] = mapped_column(LONGTEXT().with_variant(TEXT, 'postgresql'), comment='备注')
