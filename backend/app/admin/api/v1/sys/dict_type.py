#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from backend.app.admin.schema.dict_type import CreateDictTypeParam, GetDictTypeListDetails, UpdateDictTypeParam
from backend.app.admin.service.dict_type_service import dict_type_service
from backend.common.pagination import DependsPagination, paging_data
from backend.common.response.response_schema import ResponseModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db_mysql import CurrentSession

router = APIRouter()


@router.get(
    '',
    summary='（模糊条件）分页获取所有字典类型',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_pagination_dict_types(
    db: CurrentSession,
    name: Annotated[str | None, Query()] = None,
    code: Annotated[str | None, Query()] = None,
    status: Annotated[int | None, Query()] = None,
) -> ResponseModel:
    dict_type_select = await dict_type_service.get_select(name=name, code=code, status=status)
    page_data = await paging_data(db, dict_type_select, GetDictTypeListDetails)
    return await response_base.success(data=page_data)


@router.post(
    '',
    summary='创建字典类型',
    dependencies=[
        Depends(RequestPermission('sys:dict:type:add')),
        DependsRBAC,
    ],
)
async def create_dict_type(obj: CreateDictTypeParam) -> ResponseModel:
    await dict_type_service.create(obj=obj)
    return await response_base.success()


@router.put(
    '/{pk}',
    summary='更新字典类型',
    dependencies=[
        Depends(RequestPermission('sys:dict:type:edit')),
        DependsRBAC,
    ],
)
async def update_dict_type(pk: Annotated[int, Path(...)], obj: UpdateDictTypeParam) -> ResponseModel:
    count = await dict_type_service.update(pk=pk, obj=obj)
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
async def delete_dict_type(pk: Annotated[list[int], Query(...)]) -> ResponseModel:
    count = await dict_type_service.delete(pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()
