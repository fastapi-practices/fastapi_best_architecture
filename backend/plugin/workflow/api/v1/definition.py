from fastapi import APIRouter, Depends, Path, Query, Request

from backend.common.pagination import DependsPagination, PageData
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db import CurrentSession, CurrentSessionTransaction
from backend.plugin.workflow.schema.definition import (
    CreateWorkflowDefinitionParam,
    GetWorkflowDefinitionDetail,
    PreviewWorkflowFlowResponse,
    UpdateWorkflowDefinitionParam,
)
from backend.plugin.workflow.service.definition_service import workflow_definition_service

router = APIRouter()


@router.get('', dependencies=[Depends(RequestPermission('workflow:definition:list')), DependsRBAC, DependsPagination])
async def get_definitions(db: CurrentSession) -> ResponseSchemaModel[PageData[GetWorkflowDefinitionDetail]]:
    return response_base.success(data=await workflow_definition_service.get_list(db=db))


@router.get('/available', dependencies=[DependsJwtAuth, DependsPagination])
async def get_available_definitions(db: CurrentSession) -> ResponseSchemaModel[PageData[GetWorkflowDefinitionDetail]]:
    return response_base.success(data=await workflow_definition_service.get_available_list(db=db))


@router.get('/available/{pk}', dependencies=[DependsJwtAuth])
async def get_available_definition(db: CurrentSession, pk: int = Path()) -> ResponseSchemaModel[GetWorkflowDefinitionDetail]:
    return response_base.success(data=await workflow_definition_service.get_available(db=db, pk=pk))


@router.get('/available/{pk}/preview-flow', dependencies=[DependsJwtAuth])
async def preview_available_definition_flow(
    db: CurrentSession,
    request: Request,
    pk: int = Path(),
    form_data: str | None = Query(default=None),
) -> ResponseSchemaModel[PreviewWorkflowFlowResponse]:
    definition = await workflow_definition_service.get_available(db=db, pk=pk)
    payload = await workflow_definition_service.preview_flow(
        db=db,
        definition=definition,
        user_id=request.user.id,
        form_data=workflow_definition_service._parse_config(form_data),
    )
    return response_base.success(data=payload)


@router.get('/{pk}', dependencies=[Depends(RequestPermission('workflow:definition:list')), DependsRBAC])
async def get_definition(db: CurrentSession, pk: int = Path()) -> ResponseSchemaModel[GetWorkflowDefinitionDetail]:
    return response_base.success(data=await workflow_definition_service.get(db=db, pk=pk))


@router.get('/{pk}/preview-flow', dependencies=[Depends(RequestPermission('workflow:definition:list')), DependsRBAC])
async def preview_definition_flow(
    db: CurrentSession,
    request: Request,
    pk: int = Path(),
    form_data: str | None = Query(default=None),
) -> ResponseSchemaModel[PreviewWorkflowFlowResponse]:
    definition = await workflow_definition_service.get(db=db, pk=pk)
    payload = await workflow_definition_service.preview_flow(
        db=db,
        definition=definition,
        user_id=request.user.id,
        form_data=workflow_definition_service._parse_config(form_data),
    )
    return response_base.success(data=payload)


@router.post('', dependencies=[Depends(RequestPermission('workflow:definition:add')), DependsRBAC])
async def create_definition(db: CurrentSessionTransaction, obj: CreateWorkflowDefinitionParam) -> ResponseModel:
    await workflow_definition_service.create(db=db, obj=obj)
    return response_base.success()


@router.put('/{pk}', dependencies=[Depends(RequestPermission('workflow:definition:edit')), DependsRBAC])
async def update_definition(
    db: CurrentSessionTransaction,
    obj: UpdateWorkflowDefinitionParam,
    pk: int = Path(),
) -> ResponseModel:
    count = await workflow_definition_service.update(db=db, pk=pk, obj=obj)
    return response_base.success() if count > 0 else response_base.fail()
