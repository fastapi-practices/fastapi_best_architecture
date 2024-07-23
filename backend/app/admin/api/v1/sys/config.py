#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from backend.app.admin.schema.config import CreateConfigParam, GetConfigListDetails, UpdateConfigParam
from backend.app.admin.service.config_service import sys_config_service
from backend.common.pagination import DependsPagination, paging_data
from backend.common.response.response_schema import ResponseModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db_mysql import CurrentSession

router = APIRouter()


@router.get('/{pk}', summary='获取系统配置详情', dependencies=[DependsJwtAuth])
async def get_sys_config(pk: Annotated[int, Path(...)]) -> ResponseModel:
    sys_config = await sys_config_service.get(pk=pk)
    return await response_base.success(data=sys_config)


@router.get(
    '',
    summary='（模糊条件）分页获取所有系统配置',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_pagination_sys_config(db: CurrentSession) -> ResponseModel:
    sys_config_select = await sys_config_service.get_select()
    page_data = await paging_data(db, sys_config_select, GetConfigListDetails)
    return await response_base.success(data=page_data)


@router.post(
    '',
    summary='创建系统配置',
    dependencies=[
        Depends(RequestPermission('sys:gen:business:add')),
        DependsRBAC,
    ],
)
async def create_sys_config(obj: CreateConfigParam) -> ResponseModel:
    await sys_config_service.create(obj=obj)
    return await response_base.success()


@router.put(
    '/{pk}',
    summary='更新系统配置',
    dependencies=[
        Depends(RequestPermission('sys:gen:business:edit')),
        DependsRBAC,
    ],
)
async def update_sys_config(pk: Annotated[int, Path(...)], obj: UpdateConfigParam) -> ResponseModel:
    count = await sys_config_service.update(pk=pk, obj=obj)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.delete(
    '',
    summary='（批量）删除系统配置',
    dependencies=[
        Depends(RequestPermission('sys:gen:business:del')),
        DependsRBAC,
    ],
)
async def delete_sys_config(pk: Annotated[list[int], Query(...)]) -> ResponseModel:
    count = await sys_config_service.delete(pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()
