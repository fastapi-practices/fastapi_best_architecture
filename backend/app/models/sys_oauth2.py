#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.models.base import Base, id_key


class OAuth2(Base):
    """用户 OAuth2 表"""

    __tablename__ = 'sys_oauth2'

    id: Mapped[id_key] = mapped_column(init=False)
    user_id: Mapped[int] = mapped_column(comment='系统用户 ID')
    user_uuid: Mapped[str] = mapped_column(String(50), unique=True, comment='系统用户 UUID')
    source: Mapped[str] = mapped_column(String(20), default=None, comment='第三方用户来源')
    open_id: Mapped[str] = mapped_column(String(20), default=None, comment='第三方用户的 open id')
    uid: Mapped[str] = mapped_column(String(20), default=None, comment='第三方用户的 ID')
    union_id: Mapped[str] = mapped_column(String(20), default=None, comment='第三方用户的 union id')
    scope: Mapped[str] = mapped_column(String(120), default=None, comment='第三方用户授予的权限')
    code: Mapped[str] = mapped_column(String(50), default=None, comment='用户的授权 code')
