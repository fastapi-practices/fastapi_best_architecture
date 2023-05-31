#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Query, Request

from backend.app.common.jwt import DependsJwtAuth
from backend.app.common.pagination import paging_data, PageDepends
from backend.app.common.response.response_schema import response_base
from backend.app.database.db_mysql import CurrentSession
from backend.app.schemas.user import CreateUser, GetAllUserInfo, ResetPassword, UpdateUser, Avatar
from backend.app.services.user_service import UserService
from backend.app.utils.serializers import select_to_json

router = APIRouter()


@router.post('/register', summary='用户注册')
async def user_register(obj: CreateUser):
    await UserService.register(obj)
    return response_base.success()


@router.post('/password/reset', summary='密码重置')
async def password_reset(obj: ResetPassword):
    count = await UserService.pwd_reset(obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.get('/{username}', summary='查看用户信息', dependencies=[DependsJwtAuth])
async def get_user(username: str):
    current_user = await UserService.get_userinfo(username)
    data = GetAllUserInfo(**select_to_json(current_user))
    return response_base.success(data=data)


@router.put('/{username}', summary='更新用户信息', dependencies=[DependsJwtAuth])
async def update_userinfo(request: Request, username: str, obj: UpdateUser):
    count = await UserService.update(request=request, username=username, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.put('/{username}/avatar', summary='更新头像', dependencies=[DependsJwtAuth])
async def update_avatar(request: Request, username: str, avatar: Avatar):
    count = await UserService.update_avatar(request=request, username=username, avatar=avatar)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.get('', summary='（模糊条件）分页获取所有用户', dependencies=[DependsJwtAuth, PageDepends])
async def get_all_users(
    db: CurrentSession,
    username: Annotated[str | None, Query()] = None,
    phone: Annotated[str | None, Query()] = None,
    status: Annotated[int | None, Query()] = None,
):
    user_select = await UserService.get_select(username=username, phone=phone, status=status)
    page_data = await paging_data(db, user_select, GetAllUserInfo)
    return response_base.success(data=page_data)


@router.post('/{pk}/super', summary='修改用户超级权限', dependencies=[DependsJwtAuth])
async def super_set(request: Request, pk: int):
    count = await UserService.update_permission(request=request, pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.post('/{pk}/action', summary='修改用户状态', dependencies=[DependsJwtAuth])
async def active_set(request: Request, pk: int):
    count = await UserService.update_active(request=request, pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.post('/{pk}/multi', summary='修改用户多点登录状态')
async def multi_set(request: Request, pk: int, current_user: CurrentUser):
    count = await UserService.update_multi_login(request=request, pk=pk, current_user=current_user)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    path='/{username}',
    summary='用户注销',
    description='用户注销 != 用户登出，注销之后用户将从数据库删除',
    dependencies=[DependsJwtAuth],
)
async def delete_user(request: Request, username: str):
    count = await UserService.delete(username=username, request=request)
    if count > 0:
        return response_base.success()
    return response_base.fail()
