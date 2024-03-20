#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from backend.app.admin.schema.dict_data import CreateDictDataParam, GetDictDataListDetails, UpdateDictDataParam
from backend.app.admin.service.dict_data_service import dict_data_service
from backend.common.pagination import DependsPagination, paging_data
from backend.common.response.response_schema import ResponseModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db_mysql import CurrentSession
from backend.utils.serializers import select_as_dict

router = APIRouter()


@router.get('/{pk}', summary='获取字典详情', dependencies=[DependsJwtAuth])
async def get_dict_data(pk: Annotated[int, Path(...)]) -> ResponseModel:
    dict_data = await dict_data_service.get(pk=pk)
    data = GetDictDataListDetails(**await select_as_dict(dict_data))
    return await response_base.success(data=data)


@router.get(
    '',
    summary='（模糊条件）分页获取所有字典',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_pagination_dict_datas(
    db: CurrentSession,
    label: Annotated[str | None, Query()] = None,
    value: Annotated[str | None, Query()] = None,
    status: Annotated[int | None, Query()] = None,
) -> ResponseModel:
    dict_data_select = await dict_data_service.get_select(label=label, value=value, status=status)
    page_data = await paging_data(db, dict_data_select, GetDictDataListDetails)
    return await response_base.success(data=page_data)


@router.post(
    '',
    summary='创建字典',
    dependencies=[
        Depends(RequestPermission('sys:dict:data:add')),
        DependsRBAC,
    ],
)
async def create_dict_data(obj: CreateDictDataParam) -> ResponseModel:
    await dict_data_service.create(obj=obj)
    return await response_base.success()


@router.put(
    '/{pk}',
    summary='更新字典',
    dependencies=[
        Depends(RequestPermission('sys:dict:data:edit')),
        DependsRBAC,
    ],
)
async def update_dict_data(pk: Annotated[int, Path(...)], obj: UpdateDictDataParam) -> ResponseModel:
    count = await dict_data_service.update(pk=pk, obj=obj)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.delete(
    '',
    summary='（批量）删除字典',
    dependencies=[
        Depends(RequestPermission('sys:dict:data:del')),
        DependsRBAC,
    ],
)
async def delete_dict_data(pk: Annotated[list[int], Query(...)]) -> ResponseModel:
    count = await dict_data_service.delete(pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()
