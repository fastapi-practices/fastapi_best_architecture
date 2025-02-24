#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Union

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.common.model import Base, id_key


class Dept(Base):
    """部门表"""

    __tablename__ = 'sys_dept'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(50), comment='部门名称')
    sort: Mapped[int] = mapped_column(default=0, comment='排序')
    leader: Mapped[str | None] = mapped_column(String(20), default=None, comment='负责人')
    phone: Mapped[str | None] = mapped_column(String(11), default=None, comment='手机')
    email: Mapped[str | None] = mapped_column(String(50), default=None, comment='邮箱')
    status: Mapped[int] = mapped_column(default=1, comment='部门状态(0停用 1正常)')
    del_flag: Mapped[bool] = mapped_column(
        Boolean().with_variant(INTEGER, 'postgresql'), default=False, comment='删除标志（0删除 1存在）'
    )

    # 父级部门一对多
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey('sys_dept.id', ondelete='SET NULL'), default=None, index=True, comment='父部门ID'
    )
    parent: Mapped[Union['Dept', None]] = relationship(init=False, back_populates='children', remote_side=[id])
    children: Mapped[list['Dept'] | None] = relationship(init=False, back_populates='parent')

    # 部门用户一对多
    users: Mapped[list['User']] = relationship(init=False, back_populates='dept')  # noqa: F821
