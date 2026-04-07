import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key


class WorkflowCategory(Base):
    """审批流分类表"""

    __tablename__ = 'workflow_category'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(sa.String(64), comment='分类名称')
    code: Mapped[str] = mapped_column(sa.String(64), unique=True, index=True, comment='分类编码')
    icon: Mapped[str | None] = mapped_column(sa.String(128), default=None, comment='分类图标')
    sort: Mapped[int] = mapped_column(default=0, comment='排序')
    status: Mapped[int] = mapped_column(default=1, comment='状态（0停用 1启用）')
    remark: Mapped[str | None] = mapped_column(sa.String(255), default=None, comment='备注')
