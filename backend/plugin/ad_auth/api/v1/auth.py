from fastapi import APIRouter, Depends
from pyrate_limiter import Duration, Rate

from backend.common.response.response_schema import ResponseSchemaModel, response_base
from backend.database.db import CurrentSessionTransaction
from backend.plugin.ad_auth.schema.auth import LoginRequest, LoginResponse
from backend.plugin.ad_auth.service.ad_auth_service import ad_auth_service
from backend.utils.limiter import RateLimiter

router = APIRouter()


@router.post(
    '/login',
    summary='AD 域认证登录',
    description='使用 AD / LDAP 域账号进行认证登录',
    dependencies=[Depends(RateLimiter(Rate(5, Duration.MINUTE)))],
)
async def ad_login(
    db: CurrentSessionTransaction,
    obj: LoginRequest,
) -> ResponseSchemaModel[LoginResponse]:
    data = await ad_auth_service.login(db=db, username=obj.username, password=obj.password)
    return response_base.success(data=data)
