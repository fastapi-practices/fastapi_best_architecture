#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.common.model import Base, id_key

if TYPE_CHECKING:
    from backend.plugin.dict.model import DictType


class DictData(Base):
    """Dictionary Data Sheet"""

    __tablename__ = 'sys_dict_data'

    id: Mapped[id_key] = mapped_column(init=False)
    label: Mapped[str] = mapped_column(String(32), unique=True, comment='Dictionary Label')
    value: Mapped[str] = mapped_column(String(32), comment='Dictionary values')
    sort: Mapped[int] = mapped_column(default=0, comment='Sort')
    status: Mapped[int] = mapped_column(default=1, comment='Status (0 disabled 1)')
    remark: Mapped[str | None] = mapped_column(
        LONGTEXT().with_variant(TEXT, 'postgresql'), default=None, comment='Remarks'
    )

    # Dictionary type one pair more
    type_id: Mapped[int] = mapped_column(
        ForeignKey('sys_dict_type.id', ondelete='CASCADE'), default=0, comment='DICTIONARY TYPE ASSOCIATION ID'
    )
    type: Mapped[DictType] = relationship(init=False, back_populates='datas')
