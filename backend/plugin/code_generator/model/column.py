from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, BigInteger, ForeignKey
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.dialects.postgresql import TEXT

from backend.common.model import DataClassBase

if TYPE_CHECKING:
    from sqlalchemy.orm import Mapped

    from backend.common.model import id_key
    from backend.plugin.code_generator.model import GenBusiness


class GenColumn(DataClassBase):
    """代码生成模型列表"""

    __tablename__ = 'gen_column'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(50), comment='列名称')
    comment: Mapped[str | None] = mapped_column(String(255), default=None, comment='列描述')
    type: Mapped[str] = mapped_column(String(20), default='String', comment='SQLA 模型列类型')
    pd_type: Mapped[str] = mapped_column(String(20), default='str', comment='列类型对应的 pydantic 类型')
    default: Mapped[str | None] = mapped_column(
        LONGTEXT().with_variant(TEXT, 'postgresql'),
        default=None,
        comment='列默认值',
    )
    sort: Mapped[int | None] = mapped_column(default=1, comment='列排序')
    length: Mapped[int] = mapped_column(default=0, comment='列长度')
    is_pk: Mapped[bool] = mapped_column(default=False, comment='是否主键')
    is_nullable: Mapped[bool] = mapped_column(default=False, comment='是否可为空')

    # 代码生成业务模型列一对多
    gen_business_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('gen_business.id', ondelete='CASCADE'),
        default=0,
        comment='代码生成业务ID',
    )
    gen_business: Mapped[GenBusiness | None] = relationship(init=False, back_populates='gen_column')
