#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request

from backend.app.common.jwt import DependsJwtAuth
from backend.app.common.pagination import DependsPagination, paging_data
from backend.app.common.permission import RequestPermission
from backend.app.common.rbac import DependsRBAC
from backend.app.common.response.response_schema import response_base
from backend.app.database.db_mysql import CurrentSession
from backend.app.schemas.user import (
    AddUser,
    Avatar,
    GetAllUserInfo,
    GetCurrentUserInfo,
    RegisterUser,
    ResetPassword,
    UpdateUser,
    UpdateUserRole,
)
from backend.app.services.user_service import UserService
from backend.app.utils.serializers import select_as_dict

router = APIRouter()


@router.post('/register', summary='用户注册')
async def user_register(obj: RegisterUser):
    await UserService.register(obj=obj)
    return await response_base.success()


@router.post('/add', summary='添加用户', dependencies=[DependsRBAC])
async def add_user(request: Request, obj: AddUser):
    await UserService.add(request=request, obj=obj)
    current_user = await UserService.get_userinfo(username=obj.username)
    data = GetAllUserInfo(**await select_as_dict(current_user))
    return await response_base.success(data=data)


@router.post('/password/reset', summary='密码重置', dependencies=[DependsJwtAuth])
async def password_reset(request: Request, obj: ResetPassword):
    count = await UserService.pwd_reset(request=request, obj=obj)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.get('/me', summary='获取当前用户信息', dependencies=[DependsJwtAuth])
async def get_current_userinfo(request: Request):
    data = GetCurrentUserInfo(**await select_as_dict(request.user))
    return await response_base.success(data=data, exclude={'password'})


@router.get('/{username}', summary='查看用户信息', dependencies=[DependsJwtAuth])
async def get_user(username: str):
    current_user = await UserService.get_userinfo(username=username)
    data = GetAllUserInfo(**await select_as_dict(current_user))
    return await response_base.success(data=data)


@router.put('/{username}', summary='更新用户信息', dependencies=[DependsJwtAuth])
async def update_userinfo(request: Request, username: str, obj: UpdateUser):
    count = await UserService.update(request=request, username=username, obj=obj)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.put(
    '/{username}/role',
    summary='更新用户角色',
    dependencies=[
        Depends(RequestPermission('sys:user:role:edit')),
        DependsRBAC,
    ],
)
async def update_user_role(request: Request, username: str, obj: UpdateUserRole):
    await UserService.update_roles(request=request, username=username, obj=obj)
    return await response_base.success()


@router.put('/{username}/avatar', summary='更新头像', dependencies=[DependsJwtAuth])
async def update_avatar(request: Request, username: str, avatar: Avatar):
    count = await UserService.update_avatar(request=request, username=username, avatar=avatar)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.get(
    '',
    summary='（模糊条件）分页获取所有用户',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_all_users(
    db: CurrentSession,
    dept: Annotated[int | None, Query()] = None,
    username: Annotated[str | None, Query()] = None,
    phone: Annotated[str | None, Query()] = None,
    status: Annotated[int | None, Query()] = None,
):
    user_select = await UserService.get_select(dept=dept, username=username, phone=phone, status=status)
    page_data = await paging_data(db, user_select, GetAllUserInfo)
    return await response_base.success(data=page_data)


@router.put('/{pk}/super', summary='修改用户超级权限', dependencies=[DependsRBAC])
async def super_set(request: Request, pk: int):
    count = await UserService.update_permission(request=request, pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.put('/{pk}/staff', summary='修改用户后台登录权限', dependencies=[DependsRBAC])
async def staff_set(request: Request, pk: int):
    count = await UserService.update_staff(request=request, pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.put('/{pk}/status', summary='修改用户状态', dependencies=[DependsRBAC])
async def status_set(request: Request, pk: int):
    count = await UserService.update_status(request=request, pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.put('/{pk}/multi', summary='修改用户多点登录状态', dependencies=[DependsRBAC])
async def multi_set(request: Request, pk: int):
    count = await UserService.update_multi_login(request=request, pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.delete(
    path='/{username}',
    summary='用户注销',
    description='用户注销 != 用户登出，注销之后用户将从数据库删除',
    dependencies=[
        Depends(RequestPermission('sys:user:del')),
        DependsRBAC,
    ],
)
async def delete_user(username: str):
    count = await UserService.delete(username=username)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()
