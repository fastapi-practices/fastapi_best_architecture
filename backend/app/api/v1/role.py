#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Query

from backend.app.common.casbin_rbac import DependsRBAC
from backend.app.common.jwt import DependsJwtAuth
from backend.app.common.pagination import PageDepends, paging_data
from backend.app.common.response.response_schema import response_base
from backend.app.database.db_mysql import CurrentSession
from backend.app.schemas.role import GetAllRole, CreateRole, UpdateRole
from backend.app.services.role_service import RoleService
from backend.app.utils.serializers import select_to_json, select_to_list

router = APIRouter()


@router.get('/all', summary='获取所有角色', dependencies=[DependsJwtAuth])
async def get_all_roles():
    roles = await RoleService.get_all()
    data = select_to_list(roles)
    return await response_base.success(data=data)


@router.get('/{pk}/all', summary='获取用户所有角色', dependencies=[DependsJwtAuth])
async def get_user_all_roles(pk: int):
    roles = await RoleService.get_user_all(pk=pk)
    data = select_to_list(roles)
    return await response_base.success(data=data)


@router.get('/{pk}', summary='获取角色详情', dependencies=[DependsJwtAuth])
async def get_role(pk: int):
    role = await RoleService.get(pk=pk)
    data = GetAllRole(**select_to_json(role))
    return await response_base.success(data=data)


@router.get('', summary='（模糊条件）分页获取所有角色', dependencies=[DependsJwtAuth, PageDepends])
async def get_all_role_list(
    db: CurrentSession,
    name: Annotated[str | None, Query()] = None,
    data_scope: Annotated[int | None, Query()] = None,
    status: Annotated[int | None, Query()] = None,
):
    role_select = await RoleService.get_select(name=name, data_scope=data_scope, status=status)
    page_data = await paging_data(db, role_select, GetAllRole)
    return await response_base.success(data=page_data)


@router.post('', summary='创建角色', dependencies=[DependsRBAC])
async def create_role(obj: CreateRole):
    await RoleService.create(obj=obj)
    return await response_base.success()


@router.put('/{pk}', summary='更新角色', dependencies=[DependsRBAC])
async def update_role(pk: int, obj: UpdateRole):
    count = await RoleService.update(pk=pk, obj=obj)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.delete('', summary='（批量）删除角色', dependencies=[DependsRBAC])
async def delete_role(pk: Annotated[list[int], Query(...)]):
    count = await RoleService.delete(pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()
