#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.common.jwt import DependsJwtAuth
from backend.app.common.response.response_schema import response_base
from backend.app.utils.redis_info import redis_info

router = APIRouter()


@router.get('/redis', summary='redis 监控', dependencies=[DependsJwtAuth])
async def get_redis_info():
    data = {'info': await redis_info.get_info(), 'stats': await redis_info.get_stats()}
    return await response_base.success(data=data)
