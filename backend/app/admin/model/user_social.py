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
    """User Social Table (OAuth2)"""

    __tablename__ = 'sys_user_social'

    id: Mapped[id_key] = mapped_column(init=False)
    source: Mapped[str] = mapped_column(String(20), comment='Third-party user sources')
    open_id: Mapped[str | None] = mapped_column(String(20), default=None, comment='open id')
    uid: Mapped[str | None] = mapped_column(String(20), default=None, comment='ID OF THIRD-PARTY USER')
    union_id: Mapped[str | None] = mapped_column(String(20), default=None, comment='union id of third-party users')
    scope: Mapped[str | None] = mapped_column(String(120), default=None, comment='Authority granted by third-party users')
    code: Mapped[str | None] = mapped_column(String(50), default=None, comment='user\'s authorization code')

    # User social information is multiple
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey('sys_user.id', ondelete='SET NULL'), default=None, comment='USER LINK ID'
    )
    user: Mapped[User | None] = relationship(init=False, back_populates='socials')
