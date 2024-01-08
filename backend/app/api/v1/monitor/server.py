#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from starlette.concurrency import run_in_threadpool

from backend.app.common.jwt import DependsJwtAuth
from backend.app.common.permission import RequestPermission
from backend.app.common.response.response_schema import response_base
from backend.app.utils.server_info import server_info

router = APIRouter()


@router.get(
    '/server',
    summary='server 监控',
    dependencies=[
        Depends(RequestPermission('sys:monitor:server')),
        DependsJwtAuth,
    ],
)
async def get_server_info():
    """IO密集型任务，使用线程池尽量减少性能损耗"""
    data = {
        'cpu': await run_in_threadpool(server_info.get_cpu_info),
        'mem': await run_in_threadpool(server_info.get_mem_info),
        'sys': await run_in_threadpool(server_info.get_sys_info),
        'disk': await run_in_threadpool(server_info.get_disk_info),
        'service': await run_in_threadpool(server_info.get_service_info),
    }
    return await response_base.success(data=data)
