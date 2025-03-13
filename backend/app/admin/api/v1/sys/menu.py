#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Path, Query, Request

from backend.app.admin.schema.menu import CreateMenuParam, GetMenuDetail, UpdateMenuParam
from backend.app.admin.service.menu_service import menu_service
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC

router = APIRouter()


@router.get('/sidebar', summary='获取用户菜单展示树', dependencies=[DependsJwtAuth])
async def get_user_sidebar_tree(request: Request) -> ResponseSchemaModel[list[dict[str, Any]]]:
    menu = await menu_service.get_user_menu_tree(request=request)
    return response_base.success(data=menu)


@router.get('/{pk}', summary='获取菜单详情', dependencies=[DependsJwtAuth])
async def get_menu(pk: Annotated[int, Path(...)]) -> ResponseSchemaModel[GetMenuDetail]:
    data = await menu_service.get(pk=pk)
    return response_base.success(data=data)


@router.get('', summary='获取所有菜单展示树', dependencies=[DependsJwtAuth])
async def get_all_menus(
    title: Annotated[str | None, Query()] = None, status: Annotated[int | None, Query()] = None
) -> ResponseSchemaModel[list[dict[str, Any]]]:
    menu = await menu_service.get_menu_tree(title=title, status=status)
    return response_base.success(data=menu)


@router.post(
    '',
    summary='创建菜单',
    dependencies=[
        Depends(RequestPermission('sys:menu:add')),
        DependsRBAC,
    ],
)
async def create_menu(obj: CreateMenuParam) -> ResponseModel:
    await menu_service.create(obj=obj)
    return response_base.success()


@router.put(
    '/{pk}',
    summary='更新菜单',
    dependencies=[
        Depends(RequestPermission('sys:menu:edit')),
        DependsRBAC,
    ],
)
async def update_menu(pk: Annotated[int, Path(...)], obj: UpdateMenuParam) -> ResponseModel:
    count = await menu_service.update(pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '/{pk}',
    summary='删除菜单',
    dependencies=[
        Depends(RequestPermission('sys:menu:del')),
        DependsRBAC,
    ],
)
async def delete_menu(request: Request, pk: Annotated[int, Path(...)]) -> ResponseModel:
    count = await menu_service.delete(request=request, pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()
