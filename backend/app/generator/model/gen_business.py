#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.common.model import Base, id_key


class GenBusiness(Base):
    """代码生成业务表"""

    __tablename__ = 'sys_gen_business'

    id: Mapped[id_key] = mapped_column(init=False)
    app_name: Mapped[str] = mapped_column(String(50), comment='应用名称（英文）')
    table_name_en: Mapped[str] = mapped_column(String(255), unique=True, comment='表名称（英文）')
    table_name_zh: Mapped[str] = mapped_column(String(255), comment='表名称（中文）')
    table_simple_name_zh: Mapped[str] = mapped_column(String(255), comment='表名称（中文简称）')
    table_comment: Mapped[str | None] = mapped_column(String(255), default=None, comment='表描述')
    # relate_model_fk: Mapped[int | None] = mapped_column(default=None, comment='关联表外键')
    schema_name: Mapped[str | None] = mapped_column(String(255), default=None, comment='Schema 名称 (默认为英文表名称)')
    default_datetime_column: Mapped[bool] = mapped_column(default=True, comment='是否存在默认时间列')
    api_version: Mapped[str] = mapped_column(String(20), default='v1', comment='代码生成 api 版本，默认为 v1')
    gen_path: Mapped[str | None] = mapped_column(String(255), default=None, comment='代码生成路径（默认为 app 根路径）')
    remark: Mapped[str | None] = mapped_column(
        LONGTEXT().with_variant(TEXT, 'postgresql'), default=None, comment='备注'
    )
    # 代码生成业务模型一对多
    gen_model: Mapped[list['GenModel']] = relationship(init=False, back_populates='gen_business')  # noqa: F821
