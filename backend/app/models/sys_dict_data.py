#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.base_class import Base, id_key


class DictData(Base):
    """字典数据"""

    __tablename__ = 'sys_dict_data'

    id: Mapped[id_key] = mapped_column(init=False)
    label: Mapped[str] = mapped_column(String(32), unique=True, comment='字典标签')
    value: Mapped[str] = mapped_column(String(32), unique=True, comment='字典值')
    type_id: Mapped[int] = mapped_column(ForeignKey('sys_dict_type.id'), comment='字典类型id')
    sort: Mapped[int] = mapped_column(default=0, comment='排序')
    status: Mapped[bool] = mapped_column(default=True, comment='状态（0停用 1正常）')
    remark: Mapped[str | None] = mapped_column(LONGTEXT, default=None, comment='备注')
    # 字典数据一对多
    type: Mapped['DictType'] = relationship(init=False, back_populates='datas')  # noqa: F821
