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
from backend.plugin.dict.schema.dict_type import CreateDictTypeParam, GetDictTypeDetail, UpdateDictTypeParam
from backend.plugin.dict.service.dict_type_service import dict_type_service

router = APIRouter()


@router.get(
    '',
    summary='分页获取所有字典类型',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_pagination_dict_types(
    db: CurrentSession,
    name: Annotated[str | None, Query(description='字典类型名称')] = None,
    code: Annotated[str | None, Query(description='字典类型编码')] = None,
    status: Annotated[int | None, Query(description='状态')] = None,
) -> ResponseSchemaModel[PageData[GetDictTypeDetail]]:
    dict_type_select = await dict_type_service.get_select(name=name, code=code, status=status)
    page_data = await paging_data(db, dict_type_select)
    return response_base.success(data=page_data)


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
    return response_base.success()


@router.put(
    '/{pk}',
    summary='更新字典类型',
    dependencies=[
        Depends(RequestPermission('sys:dict:type:edit')),
        DependsRBAC,
    ],
)
async def update_dict_type(
    pk: Annotated[int, Path(description='字典类型 ID')], obj: UpdateDictTypeParam
) -> ResponseModel:
    count = await dict_type_service.update(pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '',
    summary='批量删除字典类型',
    dependencies=[
        Depends(RequestPermission('sys:dict:type:del')),
        DependsRBAC,
    ],
)
async def delete_dict_type(pk: Annotated[list[int], Query(description='字典类型 ID 列表')]) -> ResponseModel:
    count = await dict_type_service.delete(pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()
