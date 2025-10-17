from fastapi import APIRouter

from backend.common.response.response_schema import ResponseModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.utils.redis_info import redis_info

router = APIRouter()


@router.get('', summary='redis 监控', dependencies=[DependsJwtAuth])
async def get_redis_info() -> ResponseModel:
    data = {
        'info': await redis_info.get_info(),
        'stats': await redis_info.get_stats(),
    }
    return response_base.success(data=data)
