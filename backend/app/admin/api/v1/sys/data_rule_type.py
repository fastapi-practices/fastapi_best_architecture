#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from backend.app.admin.schema.data_rule_type import (
    CreateDataRuleTypeParam,
    GetDataRuleTypeListDetails,
    UpdateDataRuleTypeParam,
)
from backend.app.admin.service.data_rule_type_service import data_rule_type_service
from backend.common.pagination import DependsPagination, paging_data
from backend.common.response.response_schema import ResponseModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db_mysql import CurrentSession
from backend.utils.serializers import select_as_dict

router = APIRouter()


@router.get('/{pk}', summary='获取数据权限规则类型详情', dependencies=[DependsJwtAuth])
async def get_data_rule_type(pk: Annotated[int, Path(...)]) -> ResponseModel:
    data_rule_type = await data_rule_type_service.get(pk=pk)
    data = GetDataRuleTypeListDetails(**select_as_dict(data_rule_type))
    return response_base.success(data=data)


@router.get(
    '',
    summary='（模糊条件）分页获取所有数据权限规则类型',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_pagination_data_rule_type(db: CurrentSession) -> ResponseModel:
    data_rule_type_select = await data_rule_type_service.get_select()
    page_data = await paging_data(db, data_rule_type_select, GetDataRuleTypeListDetails)
    return response_base.success(data=page_data)


@router.post(
    '',
    summary='创建数据权限规则类型',
    dependencies=[
        Depends(RequestPermission('data:rule:type:add')),
        DependsRBAC,
    ],
)
async def create_data_rule_type(obj: CreateDataRuleTypeParam) -> ResponseModel:
    await data_rule_type_service.create(obj=obj)
    return response_base.success()


@router.put(
    '/{pk}',
    summary='更新数据权限规则类型',
    dependencies=[
        Depends(RequestPermission('data:rule:type:edit')),
        DependsRBAC,
    ],
)
async def update_data_rule_type(pk: Annotated[int, Path(...)], obj: UpdateDataRuleTypeParam) -> ResponseModel:
    count = await data_rule_type_service.update(pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '',
    summary='（批量）删除数据权限规则类型',
    dependencies=[
        Depends(RequestPermission('data:rule:type:del')),
        DependsRBAC,
    ],
)
async def delete_data_rule_type(pk: Annotated[list[int], Query(...)]) -> ResponseModel:
    count = await data_rule_type_service.delete(pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()
