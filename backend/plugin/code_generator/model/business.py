#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.common.model import Base, id_key

if TYPE_CHECKING:
    from backend.plugin.code_generator.model import GenColumn


class GenBusiness(Base):
    """Code Generation Business Sheet"""

    __tablename__ = 'gen_business'

    id: Mapped[id_key] = mapped_column(init=False)
    app_name: Mapped[str] = mapped_column(String(50), comment='Application name (English)')
    table_name: Mapped[str] = mapped_column(String(255), unique=True, comment='Table name (English)')
    doc_comment: Mapped[str] = mapped_column(String(255), comment='Document Comment (for function/parameter documents)')
    table_comment: Mapped[str | None] = mapped_column(String(255), default=None, comment='Table Description')
    # relate_model_fk: Mapped[int | None] = mapped_column(default=None, comment='Associated external keys')
    class_name: Mapped[str | None] = mapped_column(String(50), default=None, comment='Base class name (defaultly English Table name)')
    schema_name: Mapped[str | None] = mapped_column(String(50), default=None, comment='Schema Name (Default is Table Name)')
    filename: Mapped[str | None] = mapped_column(String(50), default=None, comment='Base File Name (default is the English Table Name)')
    default_datetime_column: Mapped[bool] = mapped_column(default=True, comment='Existence of default timebar')
    api_version: Mapped[str] = mapped_column(String(20), default='v1', comment='code generation api version, default v1')
    gen_path: Mapped[str | None] = mapped_column(String(255), default=None, comment='code generation path (default app root path)')
    remark: Mapped[str | None] = mapped_column(
        LONGTEXT().with_variant(TEXT, 'postgresql'), default=None, comment='Remarks'
    )
    # Code Generation Business Models
    gen_column: Mapped[list['GenColumn']] = relationship(init=False, back_populates='gen_business')
