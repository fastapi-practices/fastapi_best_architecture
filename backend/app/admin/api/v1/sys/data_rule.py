#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from backend.app.admin.schema.data_rule import (
    CreateDataRuleParam,
    GetDataRuleColumnDetail,
    GetDataRuleDetail,
    UpdateDataRuleParam,
)
from backend.app.admin.service.data_rule_service import data_rule_service
from backend.common.pagination import DependsPagination, PageData, paging_data
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db import CurrentSession

router = APIRouter()


@router.get('/models', summary='Available models for access rules', dependencies=[DependsJwtAuth])
async def get_data_rule_models() -> ResponseSchemaModel[list[str]]:
    models = await data_rule_service.get_models()
    return response_base.success(data=models)


@router.get('/model/{model}/columns', summary='Acquiring data rules available model columns', dependencies=[DependsJwtAuth])
async def get_data_rule_model_columns(
    model: Annotated[str, Path(description='Model Name')],
) -> ResponseSchemaModel[list[GetDataRuleColumnDetail]]:
    models = await data_rule_service.get_columns(model=model)
    return response_base.success(data=models)


@router.get('/all', summary='Access to all data rules', dependencies=[DependsJwtAuth])
async def get_all_data_rules() -> ResponseSchemaModel[list[GetDataRuleDetail]]:
    data = await data_rule_service.get_all()
    return response_base.success(data=data)


@router.get('/{pk}', summary='Details of access rules', dependencies=[DependsJwtAuth])
async def get_data_rule(
    pk: Annotated[int, Path(description='DATA RULE ID')],
) -> ResponseSchemaModel[GetDataRuleDetail]:
    data = await data_rule_service.get(pk=pk)
    return response_base.success(data=data)


@router.get(
    '',
    summary='Page Break All Data Rules',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_pagination_data_rules(
    db: CurrentSession, name: Annotated[str | None, Query(description='Rule name')] = None
) -> ResponseSchemaModel[PageData[GetDataRuleDetail]]:
    data_rule_select = await data_rule_service.get_select(name=name)
    page_data = await paging_data(db, data_rule_select)
    return response_base.success(data=page_data)


@router.post(
    '',
    summary='Create Data Rules',
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
    summary='Update Data Rules',
    dependencies=[
        Depends(RequestPermission('data:rule:edit')),
        DependsRBAC,
    ],
)
async def update_data_rule(
    pk: Annotated[int, Path(description='DATA RULE ID')], obj: UpdateDataRuleParam
) -> ResponseModel:
    count = await data_rule_service.update(pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '',
    summary='Batch Delete Data Rules',
    dependencies=[
        Depends(RequestPermission('data:rule:del')),
        DependsRBAC,
    ],
)
async def delete_data_rule(pk: Annotated[list[int], Query(description='DATA RULE ID LIST')]) -> ResponseModel:
    count = await data_rule_service.delete(pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()
