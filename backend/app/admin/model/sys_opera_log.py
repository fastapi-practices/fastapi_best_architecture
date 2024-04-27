#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import String
from sqlalchemy.dialects.mysql import JSON, LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import DataClassBase, id_key
from backend.utils.timezone import timezone


class OperaLog(DataClassBase):
    """操作日志表"""

    __tablename__ = 'sys_opera_log'

    id: Mapped[id_key] = mapped_column(init=False)
    username: Mapped[str | None] = mapped_column(String(20), comment='用户名')
    method: Mapped[str] = mapped_column(String(20), comment='请求类型')
    title: Mapped[str] = mapped_column(String(255), comment='操作模块')
    path: Mapped[str] = mapped_column(String(500), comment='请求路径')
    ip: Mapped[str] = mapped_column(String(50), comment='IP地址')
    country: Mapped[str | None] = mapped_column(String(50), comment='国家')
    region: Mapped[str | None] = mapped_column(String(50), comment='地区')
    city: Mapped[str | None] = mapped_column(String(50), comment='城市')
    user_agent: Mapped[str] = mapped_column(String(255), comment='请求头')
    os: Mapped[str | None] = mapped_column(String(50), comment='操作系统')
    browser: Mapped[str | None] = mapped_column(String(50), comment='浏览器')
    device: Mapped[str | None] = mapped_column(String(50), comment='设备')
    args: Mapped[str | None] = mapped_column(JSON(), comment='请求参数')
    status: Mapped[int] = mapped_column(comment='操作状态（0异常 1正常）')
    code: Mapped[str] = mapped_column(String(20), insert_default='200', comment='操作状态码')
    msg: Mapped[str | None] = mapped_column(LONGTEXT, comment='提示消息')
    cost_time: Mapped[float] = mapped_column(insert_default=0.0, comment='请求耗时ms')
    opera_time: Mapped[datetime] = mapped_column(comment='操作时间')
    created_time: Mapped[datetime] = mapped_column(init=False, default_factory=timezone.now, comment='创建时间')
