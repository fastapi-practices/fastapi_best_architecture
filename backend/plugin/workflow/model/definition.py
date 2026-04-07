import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, UniversalText, id_key


class WorkflowDefinition(Base):
    """审批流定义表"""

    __tablename__ = 'workflow_definition'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(sa.String(100), comment='流程名称')
    code: Mapped[str] = mapped_column(sa.String(100), unique=True, index=True, comment='流程编码')
    category_id: Mapped[int | None] = mapped_column(sa.BigInteger, index=True, default=None, comment='分类ID')
    description: Mapped[str | None] = mapped_column(UniversalText, default=None, comment='流程描述')
    form_config: Mapped[str | None] = mapped_column(UniversalText, default=None, comment='表单配置JSON')
    flow_config: Mapped[str | None] = mapped_column(UniversalText, default=None, comment='流程配置JSON')
    status: Mapped[int] = mapped_column(default=0, comment='状态（0草稿 1发布 2停用）')
    allow_withdraw: Mapped[bool] = mapped_column(default=True, comment='是否允许撤回')
    allow_urge: Mapped[bool] = mapped_column(default=True, comment='是否允许催办')
