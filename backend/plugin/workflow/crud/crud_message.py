from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.plugin.workflow.model import WorkflowMessage


class CRUDWorkflowMessage(CRUDPlus[WorkflowMessage]):
    async def get(self, db: AsyncSession, pk: int) -> WorkflowMessage | None:
        return await self.select_model(db, pk)

    async def get_select_by_receiver(self, receiver_id: int) -> Select:
        return await self.select_order('id', 'desc', receiver_id=receiver_id)

    async def get_select_by_instance(self, instance_id: int) -> Select:
        return await self.select_order('id', 'desc', instance_id=instance_id)


workflow_message_dao: CRUDWorkflowMessage = CRUDWorkflowMessage(WorkflowMessage)
