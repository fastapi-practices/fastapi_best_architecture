#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Union

from sqlalchemy import func, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.base_class import use_uuid, id_key, DataClassBase
from backend.app.models.sys_user_role import sys_user_role


class User(DataClassBase):
    """用户表"""

    __tablename__ = 'sys_user'

    id: Mapped[id_key] = mapped_column(init=False)
    user_uuid: Mapped[str] = mapped_column(String(50), init=False, insert_default=use_uuid, unique=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, index=True, comment='用户名')
    nickname: Mapped[str] = mapped_column(String(20), unique=True, comment='昵称')
    password: Mapped[str] = mapped_column(String(255), comment='密码')
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True, comment='邮箱')
    is_superuser: Mapped[bool] = mapped_column(default=False, comment='超级权限(0否 1是)')
    is_active: Mapped[bool] = mapped_column(default=True, comment='用户账号状态(0停用 1正常)')
    is_multi_login: Mapped[bool] = mapped_column(default=False, comment='是否重复登陆(0否 1是)')
    avatar: Mapped[str | None] = mapped_column(String(255), default=None, comment='头像')
    phone: Mapped[str | None] = mapped_column(String(11), default=None, comment='手机号')
    time_joined: Mapped[datetime] = mapped_column(init=False, default=func.now(), comment='注册时间')
    last_login: Mapped[datetime | None] = mapped_column(init=False, onupdate=func.now(), comment='上次登录')
    # 部门用户一对多
    dept_id: Mapped[int | None] = mapped_column(ForeignKey('sys_dept.id'), default=None, comment='部门关联ID')
    dept: Mapped[Union['Dept', None]] = relationship(init=False, back_populates='users')  # noqa: F821
    # 用户角色多对多
    roles: Mapped[list['Role']] = relationship(  # noqa: F821
        init=False, secondary=sys_user_role, back_populates='users'
    )
