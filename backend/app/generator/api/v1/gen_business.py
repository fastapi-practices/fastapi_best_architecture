#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Path

from backend.app.generator.schema.gen_business import (
    CreateGenBusinessParam,
    GetGenBusinessDetail,
    UpdateGenBusinessParam,
)
from backend.app.generator.schema.gen_model import GetGenModelDetail
from backend.app.generator.service.gen_business_service import gen_business_service
from backend.app.generator.service.gen_model_service import gen_model_service
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC

router = APIRouter()


@router.get('/all', summary='获取所有代码生成业务', dependencies=[DependsJwtAuth])
async def get_all_businesses() -> ResponseSchemaModel[list[GetGenBusinessDetail]]:
    data = await gen_business_service.get_all()
    return response_base.success(data=data)


@router.get('/{pk}', summary='获取代码生成业务详情', dependencies=[DependsJwtAuth])
async def get_business(pk: Annotated[int, Path(...)]) -> ResponseSchemaModel[GetGenBusinessDetail]:
    data = await gen_business_service.get(pk=pk)
    return response_base.success(data=data)


@router.get('/{pk}/models', summary='获取代码生成业务所有模型', dependencies=[DependsJwtAuth])
async def get_business_all_models(pk: Annotated[int, Path(...)]) -> ResponseSchemaModel[list[GetGenModelDetail]]:
    data = await gen_model_service.get_by_business(business_id=pk)
    return response_base.success(data=data)


@router.post(
    '',
    summary='创建代码生成业务',
    deprecated=True,
    dependencies=[
        Depends(RequestPermission('gen:code:business:add')),
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
        Depends(RequestPermission('gen:code:business:edit')),
        DependsRBAC,
    ],
)
async def update_business(pk: Annotated[int, Path(...)], obj: UpdateGenBusinessParam) -> ResponseModel:
    count = await gen_business_service.update(pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '/{pk}',
    summary='删除代码生成业务',
    dependencies=[
        Depends(RequestPermission('gen:code:business:del')),
        DependsRBAC,
    ],
)
async def delete_business(pk: Annotated[int, Path(...)]) -> ResponseModel:
    count = await gen_business_service.delete(pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()
