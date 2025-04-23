#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Path, Query

from backend.app.admin.schema.dept import CreateDeptParam, GetDeptDetail, UpdateDeptParam
from backend.app.admin.service.dept_service import dept_service
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC

router = APIRouter()


@router.get('/{pk}', summary='获取部门详情', dependencies=[DependsJwtAuth])
async def get_dept(pk: Annotated[int, Path(description='部门 ID')]) -> ResponseSchemaModel[GetDeptDetail]:
    data = await dept_service.get(pk=pk)
    return response_base.success(data=data)


@router.get('', summary='获取所有部门展示树', dependencies=[DependsJwtAuth])
async def get_all_depts(
    name: Annotated[str | None, Query(description='部门名称')] = None,
    leader: Annotated[str | None, Query(description='部门负责人')] = None,
    phone: Annotated[str | None, Query(description='联系电话')] = None,
    status: Annotated[int | None, Query(description='状态')] = None,
) -> ResponseSchemaModel[list[dict[str, Any]]]:
    dept = await dept_service.get_dept_tree(name=name, leader=leader, phone=phone, status=status)
    return response_base.success(data=dept)


@router.post(
    '',
    summary='创建部门',
    dependencies=[
        Depends(RequestPermission('sys:dept:add')),
        DependsRBAC,
    ],
)
async def create_dept(obj: CreateDeptParam) -> ResponseModel:
    await dept_service.create(obj=obj)
    return response_base.success()


@router.put(
    '/{pk}',
    summary='更新部门',
    dependencies=[
        Depends(RequestPermission('sys:dept:edit')),
        DependsRBAC,
    ],
)
async def update_dept(pk: Annotated[int, Path(description='部门 ID')], obj: UpdateDeptParam) -> ResponseModel:
    count = await dept_service.update(pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '/{pk}',
    summary='删除部门',
    dependencies=[
        Depends(RequestPermission('sys:dept:del')),
        DependsRBAC,
    ],
)
async def delete_dept(pk: Annotated[int, Path(description='部门 ID')]) -> ResponseModel:
    count = await dept_service.delete(pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()
