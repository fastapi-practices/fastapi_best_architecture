#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from backend.app.common.jwt import DependsJwtAuth
from backend.app.common.pagination import DependsPagination, paging_data
from backend.app.common.permission import RequestPermission
from backend.app.common.rbac import DependsRBAC
from backend.app.common.response.response_schema import response_base
from backend.app.database.db_mysql import CurrentSession
from backend.app.schemas.api import CreateApi, GetAllApi, UpdateApi
from backend.app.services.api_service import ApiService

router = APIRouter()


@router.get('/all', summary='获取所有接口', dependencies=[DependsJwtAuth])
async def get_all_apis():
    data = await ApiService.get_all()
    return await response_base.success(data=data)


@router.get('/{pk}', summary='获取接口详情', dependencies=[DependsJwtAuth])
async def get_api(pk: int):
    api = await ApiService.get(pk=pk)
    return await response_base.success(data=api)


@router.get(
    '',
    summary='（模糊条件）分页获取所有接口',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_api_list(
    db: CurrentSession,
    name: Annotated[str | None, Query()] = None,
    method: Annotated[str | None, Query()] = None,
    path: Annotated[str | None, Query()] = None,
):
    api_select = await ApiService.get_select(name=name, method=method, path=path)
    page_data = await paging_data(db, api_select, GetAllApi)
    return await response_base.success(data=page_data)


@router.post(
    '',
    summary='创建接口',
    dependencies=[
        Depends(RequestPermission('sys:api:add')),
        DependsRBAC,
    ],
)
async def create_api(obj: CreateApi):
    await ApiService.create(obj=obj)
    return await response_base.success()


@router.put(
    '/{pk}',
    summary='更新接口',
    dependencies=[
        Depends(RequestPermission('sys:api:edit')),
        DependsRBAC,
    ],
)
async def update_api(pk: int, obj: UpdateApi):
    count = await ApiService.update(pk=pk, obj=obj)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.delete(
    '',
    summary='（批量）删除接口',
    dependencies=[
        Depends(RequestPermission('sys:api:del')),
        DependsRBAC,
    ],
)
async def delete_api(pk: Annotated[list[int], Query(...)]):
    count = await ApiService.delete(pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()
