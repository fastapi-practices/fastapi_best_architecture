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
from backend.app.schemas.dict_type import CreateDictType, GetAllDictType, UpdateDictType
from backend.app.services.dict_type_service import DictTypeService

router = APIRouter()


@router.get(
    '',
    summary='（模糊条件）分页获取所有字典类型',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_all_dict_types(
    db: CurrentSession,
    name: Annotated[str | None, Query()] = None,
    code: Annotated[str | None, Query()] = None,
    status: Annotated[int | None, Query()] = None,
):
    dict_type_select = await DictTypeService.get_select(name=name, code=code, status=status)
    page_data = await paging_data(db, dict_type_select, GetAllDictType)
    return await response_base.success(data=page_data)


@router.post(
    '',
    summary='创建字典类型',
    dependencies=[
        Depends(RequestPermission('sys:dict:type:add')),
        DependsRBAC,
    ],
)
async def create_dict_type(obj: CreateDictType):
    await DictTypeService.create(obj=obj)
    return await response_base.success()


@router.put(
    '/{pk}',
    summary='更新字典类型',
    dependencies=[
        Depends(RequestPermission('sys:dict:type:edit')),
        DependsRBAC,
    ],
)
async def update_dict_type(pk: int, obj: UpdateDictType):
    count = await DictTypeService.update(pk=pk, obj=obj)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.delete(
    '',
    summary='（批量）删除字典类型',
    dependencies=[
        Depends(RequestPermission('sys:dict:type:del')),
        DependsRBAC,
    ],
)
async def delete_dict_type(pk: Annotated[list[int], Query(...)]):
    count = await DictTypeService.delete(pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()
