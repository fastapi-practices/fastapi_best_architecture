#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database.base_class import DataClassBase, id_key


class LoginLog(DataClassBase):
    """登录日志表"""

    __tablename__ = 'sys_login_log'

    id: Mapped[id_key] = mapped_column(init=False)
    user_uuid: Mapped[str] = mapped_column(String(50), comment='用户UUID')
    username: Mapped[str] = mapped_column(String(20), comment='用户名')
    status: Mapped[bool] = mapped_column(insert_default=0, comment='登录状态(0失败 1成功)')
    ipaddr: Mapped[str] = mapped_column(String(50), comment='登录IP地址')
    location: Mapped[str] = mapped_column(String(50), comment='归属地')
    browser: Mapped[str] = mapped_column(String(50), comment='浏览器')
    os: Mapped[str] = mapped_column(String(50), comment='操作系统')
    msg: Mapped[str] = mapped_column(String(255), comment='提示消息')
    login_time: Mapped[datetime] = mapped_column(comment='登录时间')
    create_time: Mapped[datetime] = mapped_column(init=False, default=func.now(), comment='创建时间')
