#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import Query, Request

from backend.app.common.pagination import paging_data
from backend.app.common.response.response_schema import response_base
from backend.app.database.db_mysql import CurrentSession
from backend.app.schemas.role import GetAllRole, CreateRole, UpdateRole
from backend.app.services.role_service import RoleService
from backend.app.utils.serializers import select_to_json


async def get_role(pk: int):
    """获取角色"""
    role = await RoleService.get(pk=pk)
    data = GetAllRole(**select_to_json(role))
    return await response_base.success(data=data)


async def get_all_roles(
    db: CurrentSession,
    name: Annotated[str | None, Query()] = None,
    data_scope: Annotated[int | None, Query()] = None,
):
    """（模糊条件）获取所有角色"""
    role_select = await RoleService.get_select(name=name, data_scope=data_scope)
    page_data = await paging_data(db, role_select, GetAllRole)
    return await response_base.success(data=page_data)


async def create_role(request: Request, obj: CreateRole):
    """创建角色"""
    await RoleService.create(obj=obj, user_id=request.user.id)
    return await response_base.success()


async def update_role(request: Request, pk: int, obj: UpdateRole):
    """更新角色"""
    count = await RoleService.update(pk=pk, obj=obj, user_id=request.user.id)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


async def delete_role(pk: Annotated[list[int], Query(...)]):
    """删除角色"""
    count = await RoleService.delete(pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()
