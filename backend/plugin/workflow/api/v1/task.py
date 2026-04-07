from fastapi import APIRouter, Path, Request

from backend.common.response.response_schema import ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.database.db import CurrentSession, CurrentSessionTransaction
from backend.plugin.workflow.schema.task import (
    ApproveWorkflowTaskParam,
    GetWorkflowTaskDetail,
    RejectWorkflowTaskParam,
)
from backend.plugin.workflow.service.task_service import workflow_task_service

router = APIRouter()


@router.get('/{pk}', dependencies=[DependsJwtAuth])
async def get_task(db: CurrentSession, request: Request, pk: int = Path()) -> ResponseSchemaModel[GetWorkflowTaskDetail]:
    return response_base.success(data=await workflow_task_service.get(db=db, pk=pk, user_id=request.user.id))


@router.post('/{pk}/approve', dependencies=[DependsJwtAuth])
async def approve_task(
    db: CurrentSessionTransaction,
    request: Request,
    obj: ApproveWorkflowTaskParam,
    pk: int = Path(),
) -> ResponseSchemaModel[GetWorkflowTaskDetail]:
    return response_base.success(data=await workflow_task_service.approve(db=db, pk=pk, user_id=request.user.id, obj=obj))


@router.post('/{pk}/reject', dependencies=[DependsJwtAuth])
async def reject_task(
    db: CurrentSessionTransaction,
    request: Request,
    obj: RejectWorkflowTaskParam,
    pk: int = Path(),
) -> ResponseSchemaModel[GetWorkflowTaskDetail]:
    return response_base.success(data=await workflow_task_service.reject(db=db, pk=pk, user_id=request.user.id, obj=obj))
