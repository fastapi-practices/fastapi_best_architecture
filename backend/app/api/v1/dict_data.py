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
from backend.app.schemas.dict_data import CreateDictData, GetAllDictData, UpdateDictData
from backend.app.services.dict_data_service import DictDataService
from backend.app.utils.serializers import select_as_dict

router = APIRouter()


@router.get('/{pk}', summary='获取字典详情', dependencies=[DependsJwtAuth])
async def get_dict_data(pk: int):
    dict_data = await DictDataService.get(pk=pk)
    data = GetAllDictData(**await select_as_dict(dict_data))
    return await response_base.success(data=data)


@router.get(
    '',
    summary='（模糊条件）分页获取所有字典',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_all_dict_datas(
    db: CurrentSession,
    label: Annotated[str | None, Query()] = None,
    value: Annotated[str | None, Query()] = None,
    status: Annotated[int | None, Query()] = None,
):
    dict_data_select = await DictDataService.get_select(label=label, value=value, status=status)
    page_data = await paging_data(db, dict_data_select, GetAllDictData)
    return await response_base.success(data=page_data)


@router.post(
    '',
    summary='创建字典',
    dependencies=[
        Depends(RequestPermission('sys:dict:data:add')),
        DependsRBAC,
    ],
)
async def create_dict_data(obj: CreateDictData):
    await DictDataService.create(obj=obj)
    return await response_base.success()


@router.put(
    '/{pk}',
    summary='更新字典',
    dependencies=[
        Depends(RequestPermission('sys:dict:data:edit')),
        DependsRBAC,
    ],
)
async def update_dict_data(pk: int, obj: UpdateDictData):
    count = await DictDataService.update(pk=pk, obj=obj)
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
async def delete_dict_data(pk: Annotated[list[int], Query(...)]):
    count = await DictDataService.delete(pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()
