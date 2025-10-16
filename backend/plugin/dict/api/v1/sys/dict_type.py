from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from backend.common.pagination import DependsPagination, PageData
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db import CurrentSession, CurrentSessionTransaction
from backend.plugin.dict.schema.dict_type import (
    CreateDictTypeParam,
    DeleteDictTypeParam,
    GetDictTypeDetail,
    UpdateDictTypeParam,
)
from backend.plugin.dict.service.dict_type_service import dict_type_service

router = APIRouter()


@router.get('/all', summary='获取所有字典数据', dependencies=[DependsJwtAuth])
async def get_all_dict_types(db: CurrentSession) -> ResponseSchemaModel[list[GetDictTypeDetail]]:
    data = await dict_type_service.get_all(db=db)
    return response_base.success(data=data)


@router.get('/{pk}', summary='获取字典类型详情', dependencies=[DependsJwtAuth])
async def get_dict_type(
    db: CurrentSession,
    pk: Annotated[int, Path(description='字典类型 ID')],
) -> ResponseSchemaModel[GetDictTypeDetail]:
    data = await dict_type_service.get(db=db, pk=pk)
    return response_base.success(data=data)


@router.get(
    '',
    summary='分页获取所有字典类型',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_dict_types_paginated(
    db: CurrentSession,
    name: Annotated[str | None, Query(description='字典类型名称')] = None,
    code: Annotated[str | None, Query(description='字典类型编码')] = None,
) -> ResponseSchemaModel[PageData[GetDictTypeDetail]]:
    page_data = await dict_type_service.get_list(db=db, name=name, code=code)
    return response_base.success(data=page_data)


@router.post(
    '',
    summary='创建字典类型',
    dependencies=[
        Depends(RequestPermission('dict:type:add')),
        DependsRBAC,
    ],
)
async def create_dict_type(db: CurrentSessionTransaction, obj: CreateDictTypeParam) -> ResponseModel:
    await dict_type_service.create(db=db, obj=obj)
    return response_base.success()


@router.put(
    '/{pk}',
    summary='更新字典类型',
    dependencies=[
        Depends(RequestPermission('dict:type:edit')),
        DependsRBAC,
    ],
)
async def update_dict_type(
    db: CurrentSessionTransaction,
    pk: Annotated[int, Path(description='字典类型 ID')],
    obj: UpdateDictTypeParam,
) -> ResponseModel:
    count = await dict_type_service.update(db=db, pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '',
    summary='批量删除字典类型',
    dependencies=[
        Depends(RequestPermission('dict:type:del')),
        DependsRBAC,
    ],
)
async def delete_dict_types(db: CurrentSessionTransaction, obj: DeleteDictTypeParam) -> ResponseModel:
    count = await dict_type_service.delete(db=db, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()
