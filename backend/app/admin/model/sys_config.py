#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key


class Config(Base):
    """系统配置表"""

    __tablename__ = 'sys_config'

    id: Mapped[id_key] = mapped_column(init=False)
    login_title: Mapped[str] = mapped_column(String(20), default='登录 FBA', comment='登录页面标题')
    login_sub_title: Mapped[str] = mapped_column(
        String(50), default='fastapi_best_architecture', comment='登录页面子标题'
    )
    footer: Mapped[str] = mapped_column(String(50), default='FBA', comment='页脚标题')
    logo: Mapped[str] = mapped_column(LONGTEXT, default='Arco', comment='Logo')
    system_title: Mapped[str] = mapped_column(String(20), default='Arco', comment='系统标题')
    system_comment: Mapped[str] = mapped_column(
        LONGTEXT,
        default='基于 FastAPI 构建的前后端分离 RBAC 权限控制系统，采用独特的伪三层架构模型设计，'
        '内置 fastapi-admin 基本实现，并作为模板库免费开源',
        comment='系统描述',
    )
