import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, UniversalText, id_key


class WorkflowInstance(Base):
    """审批流实例表"""

    __tablename__ = 'workflow_instance'

    id: Mapped[id_key] = mapped_column(init=False)
    instance_no: Mapped[str] = mapped_column(sa.String(50), unique=True, index=True, comment='实例编号')
    definition_id: Mapped[int] = mapped_column(sa.BigInteger, index=True, comment='流程定义ID')
    title: Mapped[str] = mapped_column(sa.String(200), comment='标题')
    initiator_id: Mapped[int] = mapped_column(sa.BigInteger, index=True, comment='发起人ID')
    status: Mapped[str] = mapped_column(sa.String(20), default='RUNNING', comment='实例状态')
    current_task_id: Mapped[int | None] = mapped_column(sa.BigInteger, index=True, default=None, comment='当前任务ID')
    form_data: Mapped[str | None] = mapped_column(UniversalText, default=None, comment='表单数据JSON')
    remark: Mapped[str | None] = mapped_column(UniversalText, default=None, comment='备注')
