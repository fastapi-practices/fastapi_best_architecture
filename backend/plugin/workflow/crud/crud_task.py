from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.plugin.workflow.model import WorkflowTask


class CRUDWorkflowTask(CRUDPlus[WorkflowTask]):
    async def get(self, db: AsyncSession, pk: int) -> WorkflowTask | None:
        return await self.select_model(db, pk)

    async def get_select_by_assignee(self, assignee_id: int) -> Select:
        return await self.select_order('id', 'desc', assignee_id=assignee_id)


workflow_task_dao: CRUDWorkflowTask = CRUDWorkflowTask(WorkflowTask)
