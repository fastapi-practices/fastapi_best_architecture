#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.common.model import Base, DataClassBase, id_key


class GenBusiness(Base):
    """代码生成业务表"""

    __tablename__ = 'sys_gen_business'

    id: Mapped[id_key] = mapped_column(init=False)
    app_name: Mapped[str] = mapped_column(String(50), comment='应用名称（英文）')
    model_name: Mapped[str] = mapped_column(String(255), comment='表名称（英文）')
    model_name_zh: Mapped[str] = mapped_column(String(255), comment='表名称（中文）')
    model_simple_name_zh: Mapped[str] = mapped_column(String(255), comment='表名称（中文简称）')
    model_comment: Mapped[str | None] = mapped_column(String(255), default=None, comment='表描述')
    relate_model_name: Mapped[str | None] = mapped_column(String(255), default=None, comment='关联表名称')
    relate_model_fk: Mapped[int | None] = mapped_column(default=None, comment='关联表外键')
    schema_name: Mapped[str | None] = mapped_column(String(255), default=None, comment='Schema 名称')
    gen_type: Mapped[int] = mapped_column(
        default=1, comment='代码生成方式（1：自定义路径, 2：内部写入，3：tar.gz 压缩包）'
    )
    gen_path: Mapped[str | None] = mapped_column(String(255), default=None, comment='代码生成路径（默认为项目根路径）')
    remark: Mapped[str | None] = mapped_column(LONGTEXT, default=None, comment='备注')
    # 代码生成业务model一对一
    gen_model: Mapped['GenModel'] = relationship(back_populates='gen_business')


class GenModel(DataClassBase):
    """代码生成model表"""

    __tablename__ = 'sys_gen_model'
    __table_args__ = UniqueConstraint('gen_business_id')

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(50), comment='列名称')
    comment: Mapped[str | None] = mapped_column(String(255), default=None, comment='列描述')
    type: Mapped[str] = mapped_column(String(20), default='string', comment='列类型')
    default: Mapped[str | None] = mapped_column(default=None, comment='列默认值')
    length: Mapped[int] = mapped_column(default=0, comment='列长度')
    is_pk: Mapped[bool] = mapped_column(default=False, comment='是否主键')
    is_nullable: Mapped[bool] = mapped_column(default=False, comment='是否可为空')

    # 代码生成业务model一对一
    gen_business_id: Mapped[int] = mapped_column(
        ForeignKey('sys_gen_business.id', default=None, comment='代码生成业务ID')
    )
    gen_business: Mapped['GenBusiness'] = relationship(back_populates='gen_model', single_parent=True)
