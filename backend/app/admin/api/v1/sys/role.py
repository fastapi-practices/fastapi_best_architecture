#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Path, Query

from backend.app.admin.schema.role import (
    CreateRoleParam,
    GetRoleDetail,
    GetRoleWithRelationDetail,
    UpdateRoleMenuParam,
    UpdateRoleParam,
    UpdateRoleScopeParam,
)
from backend.app.admin.service.role_service import role_service
from backend.common.pagination import DependsPagination, PageData, paging_data
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db import CurrentSession

router = APIRouter()


@router.get('/all', summary='获取所有角色', dependencies=[DependsJwtAuth])
async def get_all_roles() -> ResponseSchemaModel[list[GetRoleDetail]]:
    data = await role_service.get_all()
    return response_base.success(data=data)


@router.get('/{pk}/menus', summary='获取角色所有菜单', dependencies=[DependsJwtAuth])
async def get_role_all_menus(
    pk: Annotated[int, Path(description='角色 ID')],
) -> ResponseSchemaModel[list[dict[str, Any] | None]]:
    menu = await role_service.get_menu_tree(pk=pk)
    return response_base.success(data=menu)


@router.get('/{pk}/scopes', summary='获取角色所有数据范围', dependencies=[DependsJwtAuth])
async def get_role_all_scopes(pk: Annotated[int, Path(description='角色 ID')]) -> ResponseSchemaModel[list[int]]:
    rule = await role_service.get_scopes(pk=pk)
    return response_base.success(data=rule)


@router.get('/{pk}', summary='获取角色详情', dependencies=[DependsJwtAuth])
async def get_role(
    pk: Annotated[int, Path(description='角色 ID')],
) -> ResponseSchemaModel[GetRoleWithRelationDetail]:
    data = await role_service.get(pk=pk)
    return response_base.success(data=data)


@router.get(
    '',
    summary='分页获取所有角色',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_pagination_roles(
    db: CurrentSession,
    name: Annotated[str | None, Query(description='角色名称')] = None,
    status: Annotated[int | None, Query(description='状态')] = None,
) -> ResponseSchemaModel[PageData[GetRoleDetail]]:
    role_select = await role_service.get_select(name=name, status=status)
    page_data = await paging_data(db, role_select)
    return response_base.success(data=page_data)


@router.post(
    '',
    summary='创建角色',
    dependencies=[
        Depends(RequestPermission('sys:role:add')),
        DependsRBAC,
    ],
)
async def create_role(obj: CreateRoleParam) -> ResponseModel:
    await role_service.create(obj=obj)
    return response_base.success()


@router.put(
    '/{pk}',
    summary='更新角色',
    dependencies=[
        Depends(RequestPermission('sys:role:edit')),
        DependsRBAC,
    ],
)
async def update_role(pk: Annotated[int, Path(description='角色 ID')], obj: UpdateRoleParam) -> ResponseModel:
    count = await role_service.update(pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.put(
    '/{pk}/menus',
    summary='更新角色菜单',
    dependencies=[
        Depends(RequestPermission('sys:role:menu:edit')),
        DependsRBAC,
    ],
)
async def update_role_menus(
    pk: Annotated[int, Path(description='角色 ID')], menu_ids: UpdateRoleMenuParam
) -> ResponseModel:
    count = await role_service.update_role_menu(pk=pk, menu_ids=menu_ids)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.put(
    '/{pk}/scopes',
    summary='更新角色数据范围',
    dependencies=[
        Depends(RequestPermission('sys:role:scope:edit')),
        DependsRBAC,
    ],
)
async def update_role_scopes(
    pk: Annotated[int, Path(description='角色 ID')], scope_ids: UpdateRoleScopeParam
) -> ResponseModel:
    count = await role_service.update_role_scope(pk=pk, scope_ids=scope_ids)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '',
    summary='批量删除角色',
    dependencies=[
        Depends(RequestPermission('sys:role:del')),
        DependsRBAC,
    ],
)
async def delete_role(pk: Annotated[list[int], Query(description='角色 ID 列表')]) -> ResponseModel:
    count = await role_service.delete(pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()
