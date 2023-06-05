#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import String, func
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database.base_class import DataClassBase, id_key


class OperaLog(DataClassBase):
    """操作日志表"""

    __tablename__ = 'sys_opera_log'

    id: Mapped[id_key] = mapped_column(init=False)
    username: Mapped[str | None] = mapped_column(String(20), comment='用户名')
    method: Mapped[str] = mapped_column(String(20), comment='请求类型')
    title: Mapped[str] = mapped_column(String(255), comment='操作模块')
    path: Mapped[str] = mapped_column(String(500), comment='请求路径')
    ipaddr: Mapped[str] = mapped_column(String(50), comment='IP地址')
    location: Mapped[str] = mapped_column(String(50), comment='归属地')
    args: Mapped[str | None] = mapped_column(JSON(), comment='请求参数')
    status: Mapped[bool] = mapped_column(comment='操作状态（0异常 1正常）')
    code: Mapped[int] = mapped_column(insert_default=200, comment='操作状态码')
    msg: Mapped[str | None] = mapped_column(String(255), comment='提示消息')
    cost_time: Mapped[float] = mapped_column(insert_default=0.0, comment='请求耗时ms')
    opera_time: Mapped[datetime] = mapped_column(comment='操作时间')
    create_time: Mapped[datetime] = mapped_column(init=False, default=func.now(), comment='创建时间')
