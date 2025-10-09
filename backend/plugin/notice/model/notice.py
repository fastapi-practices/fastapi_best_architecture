from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import TEXT, String
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.mysql import LONGTEXT

from backend.common.model import Base

if TYPE_CHECKING:
    from sqlalchemy.orm import Mapped

    from backend.common.model import id_key


class Notice(Base):
    """系统通知公告表"""

    __tablename__ = 'sys_notice'

    id: Mapped[id_key] = mapped_column(init=False)
    title: Mapped[str] = mapped_column(String(50), comment='标题')
    type: Mapped[int] = mapped_column(comment='类型（0：通知、1：公告）')
    status: Mapped[int] = mapped_column(comment='状态（0：隐藏、1：显示）')
    content: Mapped[str] = mapped_column(LONGTEXT().with_variant(TEXT, 'postgresql'), comment='内容')
