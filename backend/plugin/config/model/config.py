#!/usr/bin/env python3
import sqlalchemy as sa

from sqlalchemy.dialects.mysql import LONGTEXT, TINYINT
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key


class Config(Base):
    """参数配置表"""

    __tablename__ = 'sys_config'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(sa.String(20), comment='名称')
    type: Mapped[str | None] = mapped_column(sa.String(20), server_default=None, comment='类型')
    key: Mapped[str] = mapped_column(sa.String(50), unique=True, comment='键名')
    value: Mapped[str] = mapped_column(sa.TEXT().with_variant(LONGTEXT, 'mysql'), comment='键值')
    is_frontend: Mapped[bool] = mapped_column(
        sa.INTEGER().with_variant(TINYINT, 'mysql'), default=False, comment='是否前端'
    )
    remark: Mapped[str | None] = mapped_column(sa.TEXT().with_variant(LONGTEXT, 'mysql'), default=None, comment='备注')
