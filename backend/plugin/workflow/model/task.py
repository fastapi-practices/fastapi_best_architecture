import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, UniversalText, id_key


class WorkflowTask(Base):
    """审批流任务表"""

    __tablename__ = 'workflow_task'

    id: Mapped[id_key] = mapped_column(init=False)
    instance_id: Mapped[int] = mapped_column(sa.BigInteger, index=True, comment='实例ID')
    definition_id: Mapped[int] = mapped_column(sa.BigInteger, index=True, comment='定义ID')
    task_name: Mapped[str] = mapped_column(sa.String(100), comment='任务名称')
    assignee_id: Mapped[int] = mapped_column(sa.BigInteger, index=True, comment='审批人ID')
    node_key: Mapped[str | None] = mapped_column(sa.String(100), default=None, index=True, comment='流程节点ID')
    status: Mapped[str] = mapped_column(sa.String(20), default='PENDING', comment='任务状态')
    comment: Mapped[str | None] = mapped_column(UniversalText, default=None, comment='审批意见')
    sort: Mapped[int] = mapped_column(default=1, comment='节点顺序')
    completed_time: Mapped[str | None] = mapped_column(sa.String(32), default=None, comment='完成时间')
