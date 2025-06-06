#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.common.model import Base, id_key

if TYPE_CHECKING:
    from backend.app.admin.model import User


class UserSocial(Base):
    """用户社交表（OAuth2）"""

    __tablename__ = 'sys_user_social'

    id: Mapped[id_key] = mapped_column(init=False)
    source: Mapped[str] = mapped_column(String(20), comment='第三方用户来源')
    open_id: Mapped[str | None] = mapped_column(String(20), default=None, comment='第三方用户 open id')
    sid: Mapped[str | None] = mapped_column(String(20), default=None, comment='第三方用户 ID')
    union_id: Mapped[str | None] = mapped_column(String(20), default=None, comment='第三方用户 union id')
    scope: Mapped[str | None] = mapped_column(String(120), default=None, comment='第三方用户授予的权限')
    code: Mapped[str | None] = mapped_column(String(50), default=None, comment='用户的授权 code')

    # 用户社交信息一对多
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey('sys_user.id', ondelete='SET NULL'), default=None, comment='用户关联ID'
    )
    user: Mapped[User | None] = relationship(init=False, backref='socials')
