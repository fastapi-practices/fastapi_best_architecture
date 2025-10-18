from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.common.model import Base, UniversalText, id_key

if TYPE_CHECKING:
    from backend.plugin.dict.model import DictType


class DictData(Base):
    """字典数据表"""

    __tablename__ = 'sys_dict_data'

    id: Mapped[id_key] = mapped_column(init=False)
    type_code: Mapped[str] = mapped_column(sa.String(32), comment='对应的字典类型编码')
    label: Mapped[str] = mapped_column(sa.String(32), comment='字典标签')
    value: Mapped[str] = mapped_column(sa.String(32), comment='字典值')
    color: Mapped[str | None] = mapped_column(sa.String(32), default=None, comment='标签颜色')
    sort: Mapped[int] = mapped_column(default=0, comment='排序')
    status: Mapped[int] = mapped_column(default=1, comment='状态（0停用 1正常）')
    remark: Mapped[str | None] = mapped_column(UniversalText, default=None, comment='备注')

    # 字典类型一对多
    type_id: Mapped[int] = mapped_column(
        sa.ForeignKey('sys_dict_type.id', ondelete='CASCADE'), default=0, comment='字典类型关联ID'
    )
    type: Mapped[DictType] = relationship(init=False, back_populates='datas')
