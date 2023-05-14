#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.base_class import Base, id_key


class Dept(Base):
    """部门表"""

    __tablename__ = 'sys_dept'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(50), comment='部门名称')
    parent_id: Mapped[int] = mapped_column(default=0, comment='父部门ID')
    level: Mapped[int] = mapped_column(default=0, comment='部门层级')
    sort: Mapped[int] = mapped_column(default=0, comment='排序')
    leader: Mapped[str | None] = mapped_column(String(20), default=None, comment='负责人')
    phone: Mapped[str | None] = mapped_column(String(11), default=None, comment='手机')
    email: Mapped[str | None] = mapped_column(String(50), default=None, comment='邮箱')
    status: Mapped[bool] = mapped_column(default=True, comment='部门状态(0停用 1正常)')
    del_flag: Mapped[bool] = mapped_column(default=True, comment='删除标志（0删除 1存在）')
    # 部门用户多对一
    users: Mapped['User'] = relationship(init=False, back_populates='dept')  # noqa: F821
