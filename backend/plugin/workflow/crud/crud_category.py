from collections.abc import Sequence

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.plugin.workflow.model import WorkflowCategory
from backend.plugin.workflow.schema.category import CreateWorkflowCategoryParam, UpdateWorkflowCategoryParam


class CRUDWorkflowCategory(CRUDPlus[WorkflowCategory]):
    async def get(self, db: AsyncSession, pk: int) -> WorkflowCategory | None:
        return await self.select_model(db, pk)

    async def get_all(self, db: AsyncSession) -> Sequence[WorkflowCategory]:
        return await self.select_models_order(db, 'sort', 'asc')

    async def get_select(self) -> Select:
        return await self.select_order('sort', 'asc')

    async def get_by_code(self, db: AsyncSession, code: str) -> WorkflowCategory | None:
        return await self.select_model_by_column(db, code=code)

    async def create(self, db: AsyncSession, obj: CreateWorkflowCategoryParam) -> None:
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateWorkflowCategoryParam) -> int:
        return await self.update_model(db, pk, obj)


workflow_category_dao: CRUDWorkflowCategory = CRUDWorkflowCategory(WorkflowCategory)
