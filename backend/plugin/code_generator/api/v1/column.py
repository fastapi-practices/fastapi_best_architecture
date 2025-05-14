#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Path

from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.plugin.code_generator.schema.column import CreateGenModelParam, GetGenModelDetail, UpdateGenModelParam
from backend.plugin.code_generator.service.column_service import gen_model_service

router = APIRouter()


@router.get('/types', summary='Fetch code generation model column type', dependencies=[DependsJwtAuth])
async def get_model_types() -> ResponseSchemaModel[list[str]]:
    model_types = await gen_model_service.get_types()
    return response_base.success(data=model_types)


@router.get('/{pk}', summary='Get code generation model details', dependencies=[DependsJwtAuth])
async def get_model(pk: Annotated[int, Path(description='MODEL ID')]) -> ResponseSchemaModel[GetGenModelDetail]:
    data = await gen_model_service.get(pk=pk)
    return response_base.success(data=data)


@router.post(
    '',
    summary='Create code generation model',
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
    summary='Update code generation model',
    dependencies=[
        Depends(RequestPermission('gen:code:model:edit')),
        DependsRBAC,
    ],
)
async def update_model(pk: Annotated[int, Path(description='MODEL ID')], obj: UpdateGenModelParam) -> ResponseModel:
    count = await gen_model_service.update(pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '/{pk}',
    summary='Remove Code Generation Model',
    dependencies=[
        Depends(RequestPermission('gen:code:model:del')),
        DependsRBAC,
    ],
)
async def delete_model(pk: Annotated[int, Path(description='MODEL ID')]) -> ResponseModel:
    count = await gen_model_service.delete(pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()
