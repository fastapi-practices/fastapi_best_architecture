#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from backend.app.common.jwt import DependsJwtAuth
from backend.app.common.permission import RequestPermission
from backend.app.common.rbac import DependsRBAC
from backend.app.common.response.response_schema import response_base
from backend.app.schemas.dept import CreateDept, GetAllDept, UpdateDept
from backend.app.services.dept_service import DeptService
from backend.app.utils.serializers import select_as_dict

router = APIRouter()


@router.get('/{pk}', summary='获取部门详情', dependencies=[DependsJwtAuth])
async def get_dept(pk: int):
    dept = await DeptService.get(pk=pk)
    data = GetAllDept(**await select_as_dict(dept))
    return await response_base.success(data=data)


@router.get('', summary='获取所有部门展示树', dependencies=[DependsJwtAuth])
async def get_all_depts(
    name: Annotated[str | None, Query()] = None,
    leader: Annotated[str | None, Query()] = None,
    phone: Annotated[str | None, Query()] = None,
    status: Annotated[int | None, Query()] = None,
):
    dept = await DeptService.get_dept_tree(name=name, leader=leader, phone=phone, status=status)
    return await response_base.success(data=dept)


@router.post(
    '',
    summary='创建部门',
    dependencies=[
        Depends(RequestPermission('sys:dept:add')),
        DependsRBAC,
    ],
)
async def create_dept(obj: CreateDept):
    await DeptService.create(obj=obj)
    return await response_base.success()


@router.put(
    '/{pk}',
    summary='更新部门',
    dependencies=[
        Depends(RequestPermission('sys:dept:edit')),
        DependsRBAC,
    ],
)
async def update_dept(pk: int, obj: UpdateDept):
    count = await DeptService.update(pk=pk, obj=obj)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.delete(
    '{pk}',
    summary='删除部门',
    dependencies=[
        Depends(RequestPermission('sys:dept:del')),
        DependsRBAC,
    ],
)
async def delete_dept(pk: int):
    count = await DeptService.delete(pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()
