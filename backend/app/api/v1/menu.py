#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request

from backend.app.common.jwt import DependsJwtAuth
from backend.app.common.permission import RequestPermission
from backend.app.common.rbac import DependsRBAC
from backend.app.common.response.response_schema import response_base
from backend.app.schemas.menu import CreateMenu, GetAllMenu, UpdateMenu
from backend.app.services.menu_service import MenuService
from backend.app.utils.serializers import select_as_dict

router = APIRouter()


@router.get('/sidebar', summary='获取用户菜单展示树', dependencies=[DependsJwtAuth])
async def get_user_menus(request: Request):
    menu = await MenuService.get_user_menu_tree(request=request)
    return await response_base.success(data=menu)


@router.get('/{pk}', summary='获取菜单详情', dependencies=[DependsJwtAuth])
async def get_menu(pk: int):
    menu = await MenuService.get(pk=pk)
    data = GetAllMenu(**await select_as_dict(menu))
    return await response_base.success(data=data)


@router.get('', summary='获取所有菜单展示树', dependencies=[DependsJwtAuth])
async def get_all_menus(
    title: Annotated[str | None, Query()] = None,
    status: Annotated[int | None, Query()] = None,
):
    menu = await MenuService.get_menu_tree(title=title, status=status)
    return await response_base.success(data=menu)


@router.post(
    '',
    summary='创建菜单',
    dependencies=[
        Depends(RequestPermission('sys:menu:add')),
        DependsRBAC,
    ],
)
async def create_menu(obj: CreateMenu):
    await MenuService.create(obj=obj)
    return await response_base.success()


@router.put(
    '/{pk}',
    summary='更新菜单',
    dependencies=[
        Depends(RequestPermission('sys:menu:edit')),
        DependsRBAC,
    ],
)
async def update_menu(pk: int, obj: UpdateMenu):
    count = await MenuService.update(pk=pk, obj=obj)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.delete(
    '/{pk}',
    summary='删除菜单',
    dependencies=[
        Depends(RequestPermission('sys:menu:del')),
        DependsRBAC,
    ],
)
async def delete_menu(pk: int):
    count = await MenuService.delete(pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()
