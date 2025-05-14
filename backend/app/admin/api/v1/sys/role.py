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


@router.get('/all', summary='Get All Roles', dependencies=[DependsJwtAuth])
async def get_all_roles() -> ResponseSchemaModel[list[GetRoleDetail]]:
    data = await role_service.get_all()
    return response_base.success(data=data)


@router.get('/{pk}/all', summary='Get All User Roles', dependencies=[DependsJwtAuth])
async def get_user_all_roles(
    pk: Annotated[int, Path(description='USER ID')],
) -> ResponseSchemaModel[list[GetRoleDetail]]:
    data = await role_service.get_users(pk=pk)
    return response_base.success(data=data)


@router.get('/{pk}/menus', summary='Fetch Role All Menu', dependencies=[DependsJwtAuth])
async def get_role_all_menus(
    pk: Annotated[int, Path(description='ROLE ID')],
) -> ResponseSchemaModel[list[dict[str, Any]]]:
    menu = await role_service.get_menu_tree(pk=pk)
    return response_base.success(data=menu)


@router.get('/{pk}/scopes', summary='Get all role data ranges', dependencies=[DependsJwtAuth])
async def get_role_all_scopes(pk: Annotated[int, Path(description='ROLE ID')]) -> ResponseSchemaModel[list[int]]:
    rule = await role_service.get_scopes(pk=pk)
    return response_base.success(data=rule)


@router.get('/{pk}', summary='Get Role Details', dependencies=[DependsJwtAuth])
async def get_role(
    pk: Annotated[int, Path(description='ROLE ID')],
) -> ResponseSchemaModel[GetRoleWithRelationDetail]:
    data = await role_service.get(pk=pk)
    return response_base.success(data=data)


@router.get(
    '',
    summary='Page Break For All Roles',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_pagination_roles(
    db: CurrentSession,
    name: Annotated[str | None, Query(description='Role Name')] = None,
    status: Annotated[int | None, Query(description='Status')] = None,
) -> ResponseSchemaModel[PageData[GetRoleDetail]]:
    role_select = await role_service.get_select(name=name, status=status)
    page_data = await paging_data(db, role_select)
    return response_base.success(data=page_data)


@router.post(
    '',
    summary='Create Role',
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
    summary='Update Role',
    dependencies=[
        Depends(RequestPermission('sys:role:edit')),
        DependsRBAC,
    ],
)
async def update_role(pk: Annotated[int, Path(description='ROLE ID')], obj: UpdateRoleParam) -> ResponseModel:
    count = await role_service.update(pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.put(
    '/{pk}/menu',
    summary='Update Role Menu',
    dependencies=[
        Depends(RequestPermission('sys:role:menu:edit')),
        DependsRBAC,
    ],
)
async def update_role_menus(
    pk: Annotated[int, Path(description='ROLE ID')], menu_ids: UpdateRoleMenuParam
) -> ResponseModel:
    count = await role_service.update_role_menu(pk=pk, menu_ids=menu_ids)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.put(
    '/{pk}/scope',
    summary='Update role data range',
    dependencies=[
        Depends(RequestPermission('sys:role:scope:edit')),
        DependsRBAC,
    ],
)
async def update_role_scopes(
    pk: Annotated[int, Path(description='ROLE ID')], scope_ids: UpdateRoleScopeParam
) -> ResponseModel:
    count = await role_service.update_role_scope(pk=pk, scope_ids=scope_ids)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '',
    summary='Batch Remove Roles',
    dependencies=[
        Depends(RequestPermission('sys:role:del')),
        DependsRBAC,
    ],
)
async def delete_role(pk: Annotated[list[int], Query(description='ROLE ID LIST')]) -> ResponseModel:
    count = await role_service.delete(pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()
