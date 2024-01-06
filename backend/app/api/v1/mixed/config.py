#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Request
from fastapi.routing import APIRoute

from backend.app.common.permission import RequestPermission
from backend.app.common.rbac import DependsRBAC
from backend.app.common.response.response_schema import response_base

router = APIRouter()


@router.get(
    '/routers',
    summary='获取所有路由',
    dependencies=[
        Depends(RequestPermission('sys:route:list')),
        DependsRBAC,
    ],
)
async def get_all_route(request: Request):
    data = []
    for route in request.app.routes:
        if isinstance(route, APIRoute):
            data.append(
                {
                    'path': route.path,
                    'name': route.name,
                    'summary': route.summary,
                    'methods': route.methods,
                }
            )
    return await response_base.success(data={'route_list': data})
