#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import TYPE_CHECKING, Union

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.common.model import DataClassBase, id_key

if TYPE_CHECKING:
    from backend.plugin.code_generator.model import GenBusiness


class GenColumn(DataClassBase):
    """Code Generation Model List"""

    __tablename__ = 'gen_column'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(50), comment='Column Name')
    comment: Mapped[str | None] = mapped_column(String(255), default=None, comment='Column Description')
    type: Mapped[str] = mapped_column(String(20), default='String', comment='SQLA MODEL COLUMN TYPE')
    pd_type: Mapped[str] = mapped_column(String(20), default='str', comment='pydantic type for column type')
    default: Mapped[str | None] = mapped_column(
        LONGTEXT().with_variant(TEXT, 'postgresql'), default=None, comment='Column Default'
    )
    sort: Mapped[int | None] = mapped_column(default=1, comment='Column Sort')
    length: Mapped[int] = mapped_column(default=0, comment='Column Length')
    is_pk: Mapped[bool] = mapped_column(default=False, comment='Whether the primary key')
    is_nullable: Mapped[bool] = mapped_column(default=False, comment='Could it be empty')

    # Code Generation Business Models
    gen_business_id: Mapped[int] = mapped_column(
        ForeignKey('gen_business.id', ondelete='CASCADE'), default=0, comment='CODE GENERATION BUSINESS ID'
    )
    gen_business: Mapped[Union['GenBusiness', None]] = relationship(init=False, back_populates='gen_column')
