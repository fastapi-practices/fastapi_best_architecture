#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base, id_key
from backend.app.models.sys_user_oauth2 import sys_user_oauth2


class SocialUser(Base):
    """社交用户表（OAuth2）"""

    __tablename__ = 'sys_social_user'

    id: Mapped[id_key] = mapped_column(init=False)
    uuid: Mapped[str] = mapped_column(String(50), unique=True, comment='系统用户 UUID')
    source: Mapped[str] = mapped_column(String(20), default=None, comment='第三方用户来源')
    open_id: Mapped[str] = mapped_column(String(20), default=None, comment='第三方用户的 open id')
    uid: Mapped[str] = mapped_column(String(20), default=None, comment='第三方用户的 ID')
    union_id: Mapped[str] = mapped_column(String(20), default=None, comment='第三方用户的 union id')
    scope: Mapped[str] = mapped_column(String(120), default=None, comment='第三方用户授予的权限')
    code: Mapped[str] = mapped_column(String(50), default=None, comment='用户的授权 code')
    # 用户 OAuth2 多对多
    users: Mapped[list['User']] = relationship(  # noqa: F821
        init=False, secondary=sys_user_oauth2, back_populates='social_user'
    )
