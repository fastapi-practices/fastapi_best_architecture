from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.plugin.workflow.model import WorkflowInstance


class CRUDWorkflowInstance(CRUDPlus[WorkflowInstance]):
    async def get(self, db: AsyncSession, pk: int) -> WorkflowInstance | None:
        return await self.select_model(db, pk)

    async def get_select_by_initiator(self, initiator_id: int) -> Select:
        return await self.select_order('id', 'desc', initiator_id=initiator_id)

    async def get_select_todo(self, assignee_id: int) -> Select:
        from backend.plugin.workflow.model import WorkflowTask

        instance_ids_stmt = select(WorkflowTask.instance_id).where(
            WorkflowTask.assignee_id == assignee_id,
            WorkflowTask.status == 'PENDING',
        )
        return select(WorkflowInstance).where(
            WorkflowInstance.id.in_(instance_ids_stmt)
        ).order_by(WorkflowInstance.id.desc())


workflow_instance_dao: CRUDWorkflowInstance = CRUDWorkflowInstance(WorkflowInstance)
