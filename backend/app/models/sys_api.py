#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Optional

from sqlalchemy import String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database.base_class import Base, id_key


class API(Base):
    """ 系统api """
    __tablename__ = 'sys_api'

    api_id: Mapped[id_key] = mapped_column(init=False)
    method: Mapped[str] = mapped_column(String(16), comment='请求方法')
    path: Mapped[str] = mapped_column(String(500), comment='api路径')
    remark: Mapped[str | None] = mapped_column(LONGTEXT, comment='备注')
