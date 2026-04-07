from fastapi import APIRouter, Depends, Path

from backend.common.pagination import DependsPagination, PageData
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db import CurrentSession, CurrentSessionTransaction
from backend.plugin.workflow.schema.category import (
    CreateWorkflowCategoryParam,
    GetWorkflowCategoryDetail,
    UpdateWorkflowCategoryParam,
)
from backend.plugin.workflow.service.category_service import workflow_category_service

router = APIRouter()


@router.get('', dependencies=[DependsJwtAuth, DependsPagination])
async def get_categories(db: CurrentSession) -> ResponseSchemaModel[PageData[GetWorkflowCategoryDetail]]:
    return response_base.success(data=await workflow_category_service.get_list(db=db))


@router.post('', dependencies=[Depends(RequestPermission('workflow:category:add')), DependsRBAC])
async def create_category(db: CurrentSessionTransaction, obj: CreateWorkflowCategoryParam) -> ResponseModel:
    await workflow_category_service.create(db=db, obj=obj)
    return response_base.success()


@router.put('/{pk}', dependencies=[Depends(RequestPermission('workflow:category:edit')), DependsRBAC])
async def update_category(
    db: CurrentSessionTransaction,
    obj: UpdateWorkflowCategoryParam,
    pk: int = Path(),
) -> ResponseModel:
    count = await workflow_category_service.update(db=db, pk=pk, obj=obj)
    return response_base.success() if count > 0 else response_base.fail()
