from fastapi import APIRouter, Request

from backend.common.response.response_schema import ResponseModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.database.db import CurrentSessionTransaction
from backend.plugin.oauth2.enums import UserSocialType
from backend.plugin.oauth2.service.user_social import user_social_service

router = APIRouter()


@router.delete('/me', summary='解绑用户社交账号', dependencies=[DependsJwtAuth])
async def unbinding_user(db: CurrentSessionTransaction, request: Request, source: UserSocialType) -> ResponseModel:
    await user_social_service.unbinding(db=db, user_id=request.user.id, source=source)
    return response_base.success()
