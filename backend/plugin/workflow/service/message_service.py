from sqlalchemy import func, select

from backend.common.pagination import paging_data
from backend.common.socketio.actions import workflow_message_notification
from backend.plugin.workflow.crud.crud_message import workflow_message_dao
from backend.plugin.workflow.model import WorkflowMessage


class WorkflowMessageService:
    @staticmethod
    async def get_list(*, db, user_id: int):
        return await paging_data(db, await workflow_message_dao.get_select_by_receiver(user_id))

    @staticmethod
    async def unread_count(*, db, user_id: int) -> int:
        stmt = select(func.count(WorkflowMessage.id)).where(
            WorkflowMessage.receiver_id == user_id,
            WorkflowMessage.is_read.is_(False),
        )
        return int((await db.execute(stmt)).scalar() or 0)

    @staticmethod
    async def push_message(*, db, message: WorkflowMessage) -> None:
        unread_count = await WorkflowMessageService.unread_count(db=db, user_id=message.receiver_id)
        await workflow_message_notification(
            message.receiver_id,
            {
                'id': message.id,
                'instance_id': message.instance_id,
                'task_id': message.task_id,
                'message_type': message.message_type,
                'title': message.title,
                'content': message.content,
                'is_read': message.is_read,
                'created_time': message.created_time.isoformat() if message.created_time else None,
                'unread_count': unread_count,
            },
        )

    @staticmethod
    async def mark_read(*, db, pk: int, user_id: int) -> int:
        count = await workflow_message_dao.update_model(db, pk, {'is_read': True}, receiver_id=user_id)
        if count > 0:
            await workflow_message_notification(
                user_id,
                {
                    'id': pk,
                    'type': 'READ',
                    'unread_count': await WorkflowMessageService.unread_count(db=db, user_id=user_id),
                },
            )
        return count


workflow_message_service = WorkflowMessageService()
