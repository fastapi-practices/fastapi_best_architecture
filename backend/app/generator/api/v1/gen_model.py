#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Path

from backend.app.generator.schema.gen_model import CreateGenModelParam, GetGenModelDetail, UpdateGenModelParam
from backend.app.generator.service.gen_model_service import gen_model_service
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC

router = APIRouter()


@router.get('/types', summary='获取代码生成模型列类型', dependencies=[DependsJwtAuth])
async def get_model_types() -> ResponseSchemaModel[list[str]]:
    model_types = await gen_model_service.get_types()
    return response_base.success(data=model_types)


@router.get('/{pk}', summary='获取代码生成模型详情', dependencies=[DependsJwtAuth])
async def get_model(pk: Annotated[int, Path(...)]) -> ResponseSchemaModel[GetGenModelDetail]:
    data = await gen_model_service.get(pk=pk)
    return response_base.success(data=data)


@router.post(
    '',
    summary='创建代码生成模型',
    dependencies=[
        Depends(RequestPermission('gen:code:model:add')),
        DependsRBAC,
    ],
)
async def create_model(obj: CreateGenModelParam) -> ResponseModel:
    await gen_model_service.create(obj=obj)
    return response_base.success()


@router.put(
    '/{pk}',
    summary='更新代码生成模型',
    dependencies=[
        Depends(RequestPermission('gen:code:model:edit')),
        DependsRBAC,
    ],
)
async def update_model(pk: Annotated[int, Path(...)], obj: UpdateGenModelParam) -> ResponseModel:
    count = await gen_model_service.update(pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '/{pk}',
    summary='删除代码生成模型',
    dependencies=[
        Depends(RequestPermission('gen:code:model:del')),
        DependsRBAC,
    ],
)
async def delete_model(pk: Annotated[int, Path(...)]) -> ResponseModel:
    count = await gen_model_service.delete(pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()
