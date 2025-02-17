#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, Request

from backend.common.pagination import DependsPagination, PageData, paging_data
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db import CurrentSession
from backend.plugin.casbin.schema.api import CreateApiParam, GetApiDetail, UpdateApiParam
from backend.plugin.casbin.service.api_service import api_service

router = APIRouter()


@router.get('/all', summary='获取所有接口', dependencies=[DependsJwtAuth])
async def get_all_apis() -> ResponseSchemaModel[list[GetApiDetail]]:
    data = await api_service.get_all()
    return response_base.success(data=data)


@router.get('/{pk}', summary='获取接口详情', dependencies=[DependsJwtAuth])
async def get_api(pk: Annotated[int, Path(...)]) -> ResponseSchemaModel[GetApiDetail]:
    api = await api_service.get(pk=pk)
    return response_base.success(data=api)


@router.get(
    '',
    summary='（模糊条件）分页获取所有接口',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_pagination_apis(
    request: Request,
    db: CurrentSession,
    name: Annotated[str | None, Query()] = None,
    method: Annotated[str | None, Query()] = None,
    path: Annotated[str | None, Query()] = None,
) -> ResponseSchemaModel[PageData[GetApiDetail]]:
    api_select = await api_service.get_select(request=request, name=name, method=method, path=path)
    page_data = await paging_data(db, api_select)
    return response_base.success(data=page_data)


@router.post(
    '',
    summary='创建接口',
    dependencies=[
        Depends(RequestPermission('sys:api:add')),
        DependsRBAC,
    ],
)
async def create_api(obj: CreateApiParam) -> ResponseModel:
    await api_service.create(obj=obj)
    return response_base.success()


@router.put(
    '/{pk}',
    summary='更新接口',
    dependencies=[
        Depends(RequestPermission('sys:api:edit')),
        DependsRBAC,
    ],
)
async def update_api(pk: Annotated[int, Path(...)], obj: UpdateApiParam) -> ResponseModel:
    count = await api_service.update(pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '',
    summary='（批量）删除接口',
    dependencies=[
        Depends(RequestPermission('sys:api:del')),
        DependsRBAC,
    ],
)
async def delete_api(pk: Annotated[list[int], Query(...)]) -> ResponseModel:
    count = await api_service.delete(pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()
