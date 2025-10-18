from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.common.model import Base, UniversalText, id_key

if TYPE_CHECKING:
    from backend.plugin.dict.model import DictData


class DictType(Base):
    """字典类型表"""

    __tablename__ = 'sys_dict_type'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(sa.String(32), comment='字典类型名称')
    code: Mapped[str] = mapped_column(sa.String(32), unique=True, comment='字典类型编码')
    remark: Mapped[str | None] = mapped_column(UniversalText, default=None, comment='备注')

    # 字典类型一对多
    datas: Mapped[list[DictData]] = relationship(init=False, back_populates='type')
