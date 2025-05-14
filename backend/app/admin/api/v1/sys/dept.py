#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Path, Query, Request

from backend.app.admin.schema.dept import CreateDeptParam, GetDeptDetail, UpdateDeptParam
from backend.app.admin.service.dept_service import dept_service
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC

router = APIRouter()


@router.get('/{pk}', summary='Access to sector details', dependencies=[DependsJwtAuth])
async def get_dept(pk: Annotated[int, Path(description='SECTOR ID')]) -> ResponseSchemaModel[GetDeptDetail]:
    data = await dept_service.get(pk=pk)
    return response_base.success(data=data)


@router.get('', summary='Get all sectors to show trees', dependencies=[DependsJwtAuth])
async def get_all_depts(
    request: Request,
    name: Annotated[str | None, Query(description='Department name')] = None,
    leader: Annotated[str | None, Query(description='Head of Department')] = None,
    phone: Annotated[str | None, Query(description='Call')] = None,
    status: Annotated[int | None, Query(description='Status')] = None,
) -> ResponseSchemaModel[list[dict[str, Any]]]:
    dept = await dept_service.get_dept_tree(request=request, name=name, leader=leader, phone=phone, status=status)
    return response_base.success(data=dept)


@router.post(
    '',
    summary='Create Sector',
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
    summary='Update Department',
    dependencies=[
        Depends(RequestPermission('sys:dept:edit')),
        DependsRBAC,
    ],
)
async def update_dept(pk: Annotated[int, Path(description='SECTOR ID')], obj: UpdateDeptParam) -> ResponseModel:
    count = await dept_service.update(pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '/{pk}',
    summary='Delete Sector',
    dependencies=[
        Depends(RequestPermission('sys:dept:del')),
        DependsRBAC,
    ],
)
async def delete_dept(pk: Annotated[int, Path(description='SECTOR ID')]) -> ResponseModel:
    count = await dept_service.delete(pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()
