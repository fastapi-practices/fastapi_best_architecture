#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.common.jwt import DependsJwtAuth
from backend.app.common.redis import redis_client
from backend.app.common.response.response_schema import response_base

router = APIRouter()


@router.get('/redis', summary='redis 监控', dependencies=[DependsJwtAuth])
async def redis_info():
    info = await redis_client.info()
    fmt_info = {}
    for key, value in info.items():
        if isinstance(value, dict):
            value = ','.join({f'{k}={v}' for k, v in value.items()})
        else:
            value = str(value)
        fmt_info[key] = value
    db_size = await redis_client.dbsize()
    command_stats = await redis_client.info('commandstats')
    stats_list = []
    for k, v in command_stats.items():
        stats_list.append({'name': k.split('_')[-1], 'value': str(v.get('calls', ''))})
    return await response_base.success(data={'info': fmt_info, 'stats': stats_list, 'size': db_size})
