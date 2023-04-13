#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional

from sqlalchemy import func, String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database.base_class import use_uuid, id_key, DataClassBase


class User(DataClassBase):
    """ 用户表 """
    __tablename__ = 'sys_user'

    id: Mapped[id_key] = mapped_column(init=False)
    uid: Mapped[str] = mapped_column(String(50), init=False, insert_default=use_uuid, unique=True, comment='唯一标识')
    username: Mapped[str] = mapped_column(String(20), unique=True, index=True, comment='用户名')
    password: Mapped[str] = mapped_column(String(255), comment='密码')
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True, comment='邮箱')
    is_superuser: Mapped[bool] = mapped_column(default=False, comment='超级权限')
    is_active: Mapped[bool] = mapped_column(default=True, comment='用户账号状态')
    avatar: Mapped[Optional[str]] = mapped_column(String(255), default=None, comment='头像')
    mobile_number: Mapped[Optional[str]] = mapped_column(String(11), default=None, comment='手机号')
    wechat: Mapped[Optional[str]] = mapped_column(String(20), default=None, comment='微信')
    qq: Mapped[Optional[str]] = mapped_column(String(10), default=None, comment='QQ')
    blog_address: Mapped[Optional[str]] = mapped_column(String(255), default=None, comment='博客地址')
    introduction: Mapped[Optional[str]] = mapped_column(LONGTEXT, default=None, comment='自我介绍')
    time_joined: Mapped[datetime] = mapped_column(init=False, default=func.now(), comment='注册时间')
    last_login: Mapped[Optional[datetime]] = mapped_column(init=False, onupdate=func.now(), comment='上次登录')
