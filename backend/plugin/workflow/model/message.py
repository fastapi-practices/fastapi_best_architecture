import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, UniversalText, id_key


class WorkflowMessage(Base):
    """审批流消息表"""

    __tablename__ = 'workflow_message'

    id: Mapped[id_key] = mapped_column(init=False)
    receiver_id: Mapped[int] = mapped_column(sa.BigInteger, index=True, comment='接收人ID')
    message_type: Mapped[str] = mapped_column(sa.String(40), comment='消息类型')
    title: Mapped[str] = mapped_column(sa.String(200), comment='标题')
    content: Mapped[str] = mapped_column(UniversalText, comment='内容')
    instance_id: Mapped[int | None] = mapped_column(sa.BigInteger, index=True, default=None, comment='实例ID')
    task_id: Mapped[int | None] = mapped_column(sa.BigInteger, index=True, default=None, comment='任务ID')
    is_read: Mapped[bool] = mapped_column(default=False, comment='是否已读')
