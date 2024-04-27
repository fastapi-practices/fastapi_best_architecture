#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Union

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.common.model import Base, id_key


class UserSocial(Base):
    """用户社交表（OAuth2）"""

    __tablename__ = 'sys_user_social'

    id: Mapped[id_key] = mapped_column(init=False)
    source: Mapped[str] = mapped_column(String(20), comment='第三方用户来源')
    open_id: Mapped[str | None] = mapped_column(String(20), default=None, comment='第三方用户的 open id')
    uid: Mapped[str | None] = mapped_column(String(20), default=None, comment='第三方用户的 ID')
    union_id: Mapped[str | None] = mapped_column(String(20), default=None, comment='第三方用户的 union id')
    scope: Mapped[str | None] = mapped_column(String(120), default=None, comment='第三方用户授予的权限')
    code: Mapped[str | None] = mapped_column(String(50), default=None, comment='用户的授权 code')
    # 用户 OAuth2 一对多
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey('sys_user.id', ondelete='SET NULL'), default=None, comment='用户关联ID'
    )
    user: Mapped[Union['User', None]] = relationship(init=False, back_populates='socials')  # noqa: F821
