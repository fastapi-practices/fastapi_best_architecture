from fastapi import APIRouter, Path, Request

from backend.common.pagination import DependsPagination, PageData
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.database.db import CurrentSession, CurrentSessionTransaction
from backend.plugin.workflow.schema.instance import GetWorkflowInstanceDetail, StartWorkflowInstanceParam
from backend.plugin.workflow.service.instance_service import workflow_instance_service

router = APIRouter()


@router.post('', dependencies=[DependsJwtAuth])
async def start_instance(
    db: CurrentSessionTransaction,
    request: Request,
    obj: StartWorkflowInstanceParam,
) -> ResponseSchemaModel[GetWorkflowInstanceDetail]:
    instance = await workflow_instance_service.start(db=db, obj=obj, user_id=request.user.id)
    return response_base.success(data=instance)


@router.get('/my-apply', dependencies=[DependsJwtAuth, DependsPagination])
async def get_my_apply(db: CurrentSession, request: Request) -> ResponseSchemaModel[PageData[GetWorkflowInstanceDetail]]:
    return response_base.success(data=await workflow_instance_service.get_my_apply(db=db, user_id=request.user.id))


@router.get('/my-todo', dependencies=[DependsJwtAuth, DependsPagination])
async def get_my_todo(db: CurrentSession, request: Request) -> ResponseSchemaModel[PageData[GetWorkflowInstanceDetail]]:
    return response_base.success(data=await workflow_instance_service.get_my_todo(db=db, user_id=request.user.id))


@router.get('/todo-count', dependencies=[DependsJwtAuth])
async def get_todo_count(db: CurrentSession, request: Request) -> ResponseSchemaModel[int]:
    return response_base.success(data=await workflow_instance_service.get_todo_count(db=db, user_id=request.user.id))


@router.get('/{pk}', dependencies=[DependsJwtAuth])
async def get_instance(db: CurrentSession, request: Request, pk: int = Path()) -> ResponseSchemaModel[GetWorkflowInstanceDetail]:
    return response_base.success(data=await workflow_instance_service.get_detail(db=db, pk=pk, user_id=request.user.id))


@router.post('/{pk}/withdraw', dependencies=[DependsJwtAuth])
async def withdraw_instance(
    db: CurrentSessionTransaction,
    request: Request,
    pk: int = Path(),
) -> ResponseSchemaModel[GetWorkflowInstanceDetail]:
    return response_base.success(data=await workflow_instance_service.withdraw(db=db, pk=pk, user_id=request.user.id))


@router.post('/{pk}/urge', dependencies=[DependsJwtAuth])
async def urge_instance(
    db: CurrentSessionTransaction,
    request: Request,
    pk: int = Path(),
) -> ResponseModel:
    await workflow_instance_service.urge(db=db, pk=pk, user_id=request.user.id)
    return response_base.success()
