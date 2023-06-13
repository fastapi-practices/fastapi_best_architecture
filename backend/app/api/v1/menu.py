#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Query, Request

from backend.app.common.casbin_rbac import DependsRBAC
from backend.app.common.jwt import DependsJwtAuth
from backend.app.common.response.response_schema import response_base
from backend.app.schemas.menu import GetAllMenu, CreateMenu, UpdateMenu
from backend.app.services.menu_service import MenuService
from backend.app.utils.serializers import select_to_json

router = APIRouter()


@router.get('/{pk}', summary='获取目录详情', dependencies=[DependsJwtAuth])
async def get_menu(pk: int):
    menu = await MenuService.get(pk=pk)
    data = GetAllMenu(**select_to_json(menu))
    return await response_base.success(data=data)


@router.get('', summary='获取所有目录展示树', dependencies=[DependsJwtAuth])
async def get_all_menus(
    name: Annotated[str | None, Query()] = None,
    status: Annotated[bool | None, Query()] = None,
):
    menu = await MenuService.get_select(name=name, status=status)
    return await response_base.success(data=menu)


@router.post('', summary='创建目录', dependencies=[DependsRBAC])
async def create_menu(request: Request, obj: CreateMenu):
    await MenuService.create(obj=obj, user_id=request.user.id)
    return await response_base.success()


@router.put('/{pk}', summary='更新目录', dependencies=[DependsRBAC])
async def update_menu(request: Request, pk: int, obj: UpdateMenu):
    count = await MenuService.update(pk=pk, obj=obj, user_id=request.user.id)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.delete('{pk}', summary='删除目录', dependencies=[DependsRBAC])
async def delete_menu(pk: int):
    count = await MenuService.delete(pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()
