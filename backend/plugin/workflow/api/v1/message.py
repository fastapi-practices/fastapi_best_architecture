from fastapi import APIRouter, Path, Request

from backend.common.pagination import DependsPagination, PageData
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.database.db import CurrentSession, CurrentSessionTransaction
from backend.plugin.workflow.schema.message import GetWorkflowMessageDetail
from backend.plugin.workflow.service.message_service import workflow_message_service

router = APIRouter()


@router.get('', dependencies=[DependsJwtAuth, DependsPagination])
async def get_messages(db: CurrentSession, request: Request) -> ResponseSchemaModel[PageData[GetWorkflowMessageDetail]]:
    return response_base.success(data=await workflow_message_service.get_list(db=db, user_id=request.user.id))


@router.get('/unread-count', dependencies=[DependsJwtAuth])
async def get_unread_count(db: CurrentSession, request: Request) -> ResponseSchemaModel[int]:
    return response_base.success(data=await workflow_message_service.unread_count(db=db, user_id=request.user.id))


@router.put('/{pk}/read', dependencies=[DependsJwtAuth])
async def mark_read(db: CurrentSessionTransaction, request: Request, pk: int = Path()) -> ResponseModel:
    count = await workflow_message_service.mark_read(db=db, pk=pk, user_id=request.user.id)
    return response_base.success() if count > 0 else response_base.fail()
