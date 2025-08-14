#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from backend.common.pagination import DependsPagination, PageData, paging_data
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db import CurrentSession
from backend.plugin.code_generator.schema.business import (
    CreateGenBusinessParam,
    GetGenBusinessDetail,
    UpdateGenBusinessParam,
)
from backend.plugin.code_generator.schema.column import GetGenColumnDetail
from backend.plugin.code_generator.service.business_service import gen_business_service
from backend.plugin.code_generator.service.column_service import gen_column_service

router = APIRouter()


@router.get('/all', summary='获取所有代码生成业务', dependencies=[DependsJwtAuth])
async def get_all_businesses() -> ResponseSchemaModel[list[GetGenBusinessDetail]]:
    data = await gen_business_service.get_all()
    return response_base.success(data=data)


@router.get('/{pk}', summary='获取代码生成业务详情', dependencies=[DependsJwtAuth])
async def get_business(
    pk: Annotated[int, Path(description='业务 ID')],
) -> ResponseSchemaModel[GetGenBusinessDetail]:
    data = await gen_business_service.get(pk=pk)
    return response_base.success(data=data)


@router.get(
    '',
    summary='分页获取所有代码生成业务',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_businesses_paged(
    db: CurrentSession,
    table_name: Annotated[str | None, Query(description='代码生成业务表名称')] = None,
) -> ResponseSchemaModel[PageData[GetGenBusinessDetail]]:
    business_select = await gen_business_service.get_select(table_name=table_name)
    page_data = await paging_data(db, business_select)
    return response_base.success(data=page_data)


@router.get('/{pk}/columns', summary='获取代码生成业务所有模型列', dependencies=[DependsJwtAuth])
async def get_business_all_columns(
    pk: Annotated[int, Path(description='业务 ID')],
) -> ResponseSchemaModel[list[GetGenColumnDetail]]:
    data = await gen_column_service.get_columns(business_id=pk)
    return response_base.success(data=data)


@router.post(
    '',
    summary='创建代码生成业务',
    deprecated=True,
    dependencies=[
        Depends(RequestPermission('codegen:business:add')),
        DependsRBAC,
    ],
)
async def create_business(obj: CreateGenBusinessParam) -> ResponseModel:
    await gen_business_service.create(obj=obj)
    return response_base.success()


@router.put(
    '/{pk}',
    summary='更新代码生成业务',
    dependencies=[
        Depends(RequestPermission('codegen:business:edit')),
        DependsRBAC,
    ],
)
async def update_business(
    pk: Annotated[int, Path(description='业务 ID')], obj: UpdateGenBusinessParam
) -> ResponseModel:
    count = await gen_business_service.update(pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '/{pk}',
    summary='删除代码生成业务',
    dependencies=[
        Depends(RequestPermission('codegen:business:del')),
        DependsRBAC,
    ],
)
async def delete_business(pk: Annotated[int, Path(description='业务 ID')]) -> ResponseModel:
    count = await gen_business_service.delete(pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()
