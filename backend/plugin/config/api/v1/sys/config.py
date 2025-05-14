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
from backend.plugin.config.schema.config import (
    CreateConfigParam,
    GetConfigDetail,
    SaveBuiltInConfigParam,
    UpdateConfigParam,
)
from backend.plugin.config.service.config_service import config_service

router = APIRouter()


@router.get('/website', summary='Get Site Parameter Configuration', dependencies=[DependsJwtAuth])
async def get_website_config() -> ResponseSchemaModel[list[GetConfigDetail]]:
    config = await config_service.get_built_in_config('website')
    return response_base.success(data=config)


@router.post(
    '/website',
    summary='Save Site Parameter Configuration',
    dependencies=[
        Depends(RequestPermission('sys:config:website:add')),
        DependsRBAC,
    ],
)
async def save_website_config(objs: list[SaveBuiltInConfigParam]) -> ResponseModel:
    await config_service.save_built_in_config(objs, 'website')
    return response_base.success()


@router.get('/protocol', summary='Get user protocols', dependencies=[DependsJwtAuth])
async def get_protocol_config() -> ResponseSchemaModel[list[GetConfigDetail]]:
    config = await config_service.get_built_in_config('protocol')
    return response_base.success(data=config)


@router.post(
    '/protocol',
    summary='Save user protocol',
    dependencies=[
        Depends(RequestPermission('sys:config:protocol:add')),
        DependsRBAC,
    ],
)
async def save_protocol_config(objs: list[SaveBuiltInConfigParam]) -> ResponseModel:
    await config_service.save_built_in_config(objs, 'protocol')
    return response_base.success()


@router.get('/policy', summary='Access user policy', dependencies=[DependsJwtAuth])
async def get_policy_config() -> ResponseSchemaModel[list[GetConfigDetail]]:
    config = await config_service.get_built_in_config('policy')
    return response_base.success(data=config)


@router.post(
    '/policy',
    summary='Save user policy',
    dependencies=[
        Depends(RequestPermission('sys:config:policy:add')),
        DependsRBAC,
    ],
)
async def save_policy_config(objs: list[SaveBuiltInConfigParam]) -> ResponseModel:
    await config_service.save_built_in_config(objs, 'policy')
    return response_base.success()


@router.get('/{pk}', summary='Get Parameter Configuration Details', dependencies=[DependsJwtAuth])
async def get_config(pk: Annotated[int, Path(description='PARAMETER CONFIGURATION ID')]) -> ResponseSchemaModel[GetConfigDetail]:
    config = await config_service.get(pk)
    return response_base.success(data=config)


@router.get(
    '',
    summary='Page Break Get All Parameter Configurations',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_pagination_configs(
    db: CurrentSession,
    name: Annotated[str | None, Query(description='Parameter Configuration Name')] = None,
    type: Annotated[str | None, Query()] = None,
) -> ResponseSchemaModel[PageData[GetConfigDetail]]:
    config_select = await config_service.get_select(name=name, type=type)
    page_data = await paging_data(db, config_select)
    return response_base.success(data=page_data)


@router.post(
    '',
    summary='Create Parameter Configuration',
    dependencies=[
        Depends(RequestPermission('sys:config:add')),
        DependsRBAC,
    ],
)
async def create_config(obj: CreateConfigParam) -> ResponseModel:
    await config_service.create(obj=obj)
    return response_base.success()


@router.put(
    '/{pk}',
    summary='Update Parameter Configuration',
    dependencies=[
        Depends(RequestPermission('sys:config:edit')),
        DependsRBAC,
    ],
)
async def update_config(pk: Annotated[int, Path(description='PARAMETER CONFIGURATION ID')], obj: UpdateConfigParam) -> ResponseModel:
    count = await config_service.update(pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '',
    summary='Batch Delete Parameter Configuration',
    dependencies=[
        Depends(RequestPermission('sys:config:del')),
        DependsRBAC,
    ],
)
async def delete_config(pk: Annotated[list[int], Query(description='PARAMETER CONFIGURATION ID LIST')]) -> ResponseModel:
    count = await config_service.delete(pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()
