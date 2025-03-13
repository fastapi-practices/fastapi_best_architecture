#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, Request

from backend.app.admin.schema.data_rule import CreateDataRuleParam, GetDataRuleDetail, UpdateDataRuleParam
from backend.app.admin.service.data_rule_service import data_rule_service
from backend.common.pagination import DependsPagination, PageData, paging_data
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db import CurrentSession

router = APIRouter()


@router.get('/models', summary='获取支持过滤的数据库模型', dependencies=[DependsJwtAuth])
async def get_data_rule_models() -> ResponseSchemaModel[list[str]]:
    models = await data_rule_service.get_models()
    return response_base.success(data=models)


@router.get('/model/{model}/columns', summary='获取支持过滤的数据库模型列', dependencies=[DependsJwtAuth])
async def get_data_rule_model_columns(model: Annotated[str, Path()]) -> ResponseSchemaModel[list[str]]:
    models = await data_rule_service.get_columns(model=model)
    return response_base.success(data=models)


@router.get('/all', summary='获取所有数据规则', dependencies=[DependsJwtAuth])
async def get_all_data_rule() -> ResponseSchemaModel[list[GetDataRuleDetail]]:
    data = await data_rule_service.get_all()
    return response_base.success(data=data)


@router.get('/{pk}', summary='获取数据权限规则详情', dependencies=[DependsJwtAuth])
async def get_data_rule(pk: Annotated[int, Path(...)]) -> ResponseSchemaModel[GetDataRuleDetail]:
    data = await data_rule_service.get(pk=pk)
    return response_base.success(data=data)


@router.get(
    '',
    summary='（模糊条件）分页获取所有数据权限规则',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_pagination_data_rule(
    db: CurrentSession, name: Annotated[str | None, Query()] = None
) -> ResponseSchemaModel[PageData[GetDataRuleDetail]]:
    data_rule_select = await data_rule_service.get_select(name=name)
    page_data = await paging_data(db, data_rule_select)
    return response_base.success(data=page_data)


@router.post(
    '',
    summary='创建数据权限规则',
    dependencies=[
        Depends(RequestPermission('data:rule:add')),
        DependsRBAC,
    ],
)
async def create_data_rule(obj: CreateDataRuleParam) -> ResponseModel:
    await data_rule_service.create(obj=obj)
    return response_base.success()


@router.put(
    '/{pk}',
    summary='更新数据权限规则',
    dependencies=[
        Depends(RequestPermission('data:rule:edit')),
        DependsRBAC,
    ],
)
async def update_data_rule(pk: Annotated[int, Path(...)], obj: UpdateDataRuleParam) -> ResponseModel:
    count = await data_rule_service.update(pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '',
    summary='（批量）删除数据权限规则',
    dependencies=[
        Depends(RequestPermission('data:rule:del')),
        DependsRBAC,
    ],
)
async def delete_data_rule(request: Request, pk: Annotated[list[int], Query(...)]) -> ResponseModel:
    count = await data_rule_service.delete(request=request, pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()
