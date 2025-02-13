#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import TEXT, String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key


class Notice(Base):
    """系统通知公告"""

    __tablename__ = 'sys_notice'

    id: Mapped[id_key] = mapped_column(init=False)
    title: Mapped[str] = mapped_column(String(50), comment='标题')
    type: Mapped[int] = mapped_column(comment='类型（0：通知、1：公告）')
    author: Mapped[str] = mapped_column(String(16), comment='作者')
    source: Mapped[str] = mapped_column(String(50), comment='信息来源')
    status: Mapped[int] = mapped_column(comment='状态（0：隐藏、1：显示）')
    content: Mapped[str] = mapped_column(LONGTEXT().with_variant(TEXT, 'postgresql'), comment='内容')
