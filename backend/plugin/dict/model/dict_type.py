#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.common.model import Base, id_key

if TYPE_CHECKING:
    from backend.plugin.dict.model import DictData


class DictType(Base):
    """Dictionary Type Table"""

    __tablename__ = 'sys_dict_type'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(32), comment='Dictionary Type Name')
    code: Mapped[str] = mapped_column(String(32), unique=True, comment='Dictionary type encoding')
    status: Mapped[int] = mapped_column(default=1, comment='Status (0 disabled 1)')
    remark: Mapped[str | None] = mapped_column(
        LONGTEXT().with_variant(TEXT, 'postgresql'), default=None, comment='Remarks'
    )

    # Dictionary type one pair more
    datas: Mapped[list[DictData]] = relationship(init=False, back_populates='type')
