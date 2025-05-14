#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Boolean, String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.dialects.postgresql import INTEGER, TEXT
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key


class Config(Base):
    """Parameter Configuration Table"""

    __tablename__ = 'sys_config'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(20), comment='Name')
    type: Mapped[str | None] = mapped_column(String(20), server_default=None, comment='Type')
    key: Mapped[str] = mapped_column(String(50), unique=True, comment='Keyname')
    value: Mapped[str] = mapped_column(LONGTEXT().with_variant(TEXT, 'postgresql'), comment='Key Value')
    is_frontend: Mapped[bool] = mapped_column(
        Boolean().with_variant(INTEGER, 'postgresql'), default=False, comment='Whether to frontend'
    )
    remark: Mapped[str | None] = mapped_column(
        LONGTEXT().with_variant(TEXT, 'postgresql'), default=None, comment='Remarks'
    )
