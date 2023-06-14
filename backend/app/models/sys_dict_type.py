#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.base_class import Base, id_key


class DictType(Base):
    """字典类型"""

    __tablename__ = 'sys_dict_type'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(32), unique=True, comment='字典类型名称')
    code: Mapped[str] = mapped_column(String(32), unique=True, comment='字典类型编码')
    status: Mapped[bool] = mapped_column(default=True, comment='状态（0停用 1正常）')
    remark: Mapped[str | None] = mapped_column(LONGTEXT, default=None, comment='备注')
    # 字典类型一对多
    datas: Mapped[list['DictData']] = relationship(init=False, back_populates='type')  # noqa: F821
