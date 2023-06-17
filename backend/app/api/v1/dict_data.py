#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Query, Request

from backend.app.common.casbin_rbac import DependsRBAC
from backend.app.common.pagination import PageDepends, paging_data
from backend.app.common.response.response_schema import response_base
from backend.app.database.db_mysql import CurrentSession
from backend.app.schemas.dict_data import GetAllDictData, CreateDictData, UpdateDictData
from backend.app.services.dict_data_service import DictDataService
from backend.app.utils.serializers import select_to_json

router = APIRouter()


@router.get('/{pk}', summary='获取字典详情', dependencies=[DependsRBAC])
async def get_dict_data(pk: int):
    dict_data = await DictDataService.get(pk=pk)
    data = GetAllDictData(**select_to_json(dict_data))
    return await response_base.success(data=data)


@router.get('', summary='（模糊条件）分页获取所有字典', dependencies=[DependsRBAC, PageDepends])
async def get_all_dict_datas(
    db: CurrentSession,
    label: Annotated[str | None, Query()] = None,
    value: Annotated[str | None, Query()] = None,
    status: Annotated[int | None, Query()] = None,
):
    dict_data_select = await DictDataService.get_select(label=label, value=value, status=status)
    page_data = await paging_data(db, dict_data_select, GetAllDictData)
    return await response_base.success(data=page_data)


@router.post('', summary='创建字典', dependencies=[DependsRBAC])
async def create_dict_data(request: Request, obj: CreateDictData):
    await DictDataService.create(obj=obj, user_id=request.user.id)
    return await response_base.success()


@router.put('/{pk}', summary='更新字典', dependencies=[DependsRBAC])
async def update_dict_data(request: Request, pk: int, obj: UpdateDictData):
    count = await DictDataService.update(pk=pk, obj=obj, user_id=request.user.id)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.delete('', summary='（批量）删除字典', dependencies=[DependsRBAC])
async def delete_dict_data(pk: Annotated[list[int], Query(...)]):
    count = await DictDataService.delete(pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()
