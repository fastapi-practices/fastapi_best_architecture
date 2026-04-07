from collections.abc import Sequence
from typing import Any

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.plugin.workflow.model import WorkflowDefinition
from backend.plugin.workflow.schema.definition import CreateWorkflowDefinitionParam, UpdateWorkflowDefinitionParam


class CRUDWorkflowDefinition(CRUDPlus[WorkflowDefinition]):
    async def get(self, db: AsyncSession, pk: int) -> WorkflowDefinition | None:
        return await self.select_model(db, pk)

    async def get_available(self, db: AsyncSession, pk: int) -> WorkflowDefinition | None:
        return await self.select_model_by_column(db, id=pk, status=1)

    async def get_all(self, db: AsyncSession) -> Sequence[WorkflowDefinition]:
        return await self.select_models_order(db, 'id', 'desc')

    async def get_select(self) -> Select:
        return await self.select_order('id', 'desc')

    async def get_available_select(self) -> Select:
        return await self.select_order('id', 'desc', status=1)

    async def get_by_code(self, db: AsyncSession, code: str) -> WorkflowDefinition | None:
        return await self.select_model_by_column(db, code=code)

    async def create(self, db: AsyncSession, obj: CreateWorkflowDefinitionParam | dict[str, Any]) -> None:
        payload = obj if isinstance(obj, dict) else obj.model_dump()
        db.add(self.model(**payload))

    async def update(self, db: AsyncSession, pk: int, obj: UpdateWorkflowDefinitionParam | dict[str, Any]) -> int:
        return await self.update_model(db, pk, obj)


workflow_definition_dao: CRUDWorkflowDefinition = CRUDWorkflowDefinition(WorkflowDefinition)
