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
from backend.plugin.dict.schema.dict_data import (
    CreateDictDataParam,
    DeleteDictDataParam,
    GetDictDataDetail,
    UpdateDictDataParam,
)
from backend.plugin.dict.service.dict_data_service import dict_data_service

router = APIRouter()


@router.get('/all', summary='获取所有字典数据', dependencies=[DependsJwtAuth])
async def get_all_dict_datas() -> ResponseSchemaModel[list[GetDictDataDetail]]:
    data = await dict_data_service.get_all()
    return response_base.success(data=data)


@router.get('/{pk}', summary='获取字典数据详情', dependencies=[DependsJwtAuth])
async def get_dict_data(
    pk: Annotated[int, Path(description='字典数据 ID')],
) -> ResponseSchemaModel[GetDictDataDetail]:
    data = await dict_data_service.get(pk=pk)
    return response_base.success(data=data)


@router.get('/type-codes/{code}', summary='获取字典数据列表', dependencies=[DependsJwtAuth])
async def get_dict_data_by_type_code(
    code: Annotated[str, Path(description='字典类型编码')],
) -> ResponseSchemaModel[list[GetDictDataDetail]]:
    data = await dict_data_service.get_by_type_code(code=code)
    return response_base.success(data=data)


@router.get(
    '',
    summary='分页获取所有字典数据',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_dict_datas_paged(
    db: CurrentSession,
    type_code: Annotated[str | None, Query(description='字典类型编码')] = None,
    label: Annotated[str | None, Query(description='字典数据标签')] = None,
    value: Annotated[str | None, Query(description='字典数据键值')] = None,
    status: Annotated[int | None, Query(description='状态')] = None,
    type_id: Annotated[int | None, Query(description='字典类型 ID')] = None,
) -> ResponseSchemaModel[PageData[GetDictDataDetail]]:
    dict_data_select = await dict_data_service.get_select(
        type_code=type_code, label=label, value=value, status=status, type_id=type_id
    )
    page_data = await paging_data(db, dict_data_select)
    return response_base.success(data=page_data)


@router.post(
    '',
    summary='创建字典数据',
    dependencies=[
        Depends(RequestPermission('dict:data:add')),
        DependsRBAC,
    ],
)
async def create_dict_data(obj: CreateDictDataParam) -> ResponseModel:
    await dict_data_service.create(obj=obj)
    return response_base.success()


@router.put(
    '/{pk}',
    summary='更新字典数据',
    dependencies=[
        Depends(RequestPermission('dict:data:edit')),
        DependsRBAC,
    ],
)
async def update_dict_data(
    pk: Annotated[int, Path(description='字典数据 ID')], obj: UpdateDictDataParam
) -> ResponseModel:
    count = await dict_data_service.update(pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '',
    summary='批量删除字典数据',
    dependencies=[
        Depends(RequestPermission('dict:data:del')),
        DependsRBAC,
    ],
)
async def delete_dict_datas(obj: DeleteDictDataParam) -> ResponseModel:
    count = await dict_data_service.delete(obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()
