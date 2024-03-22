#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends

from backend.common.response.response_schema import ResponseModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.utils.redis_info import redis_info

router = APIRouter()


@router.get(
    '',
    summary='redis 监控',
    dependencies=[
        Depends(RequestPermission('sys:monitor:redis')),
        DependsJwtAuth,
    ],
)
async def get_redis_info() -> ResponseModel:
    data = {'info': await redis_info.get_info(), 'stats': await redis_info.get_stats()}
    return await response_base.success(data=data)
