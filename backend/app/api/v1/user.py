#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import Query, Request

from backend.app.common.pagination import paging_data
from backend.app.common.response.response_schema import response_base
from backend.app.database.db_mysql import CurrentSession
from backend.app.schemas.user import CreateUser, GetAllUserInfo, ResetPassword, UpdateUser, Avatar
from backend.app.services.user_service import UserService
from backend.app.utils.serializers import select_to_json


async def register_user(obj: CreateUser):
    """注册用户"""
    await UserService.register(obj=obj)
    return await response_base.success()


async def reset_password(request: Request, obj: ResetPassword):
    """密码重置"""
    count = await UserService.reset_pwd(request=request, obj=obj)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


async def get_user(username: str):
    """获取用户详情"""
    current_user = await UserService.get_userinfo(username=username)
    data = GetAllUserInfo(**select_to_json(current_user))
    return await response_base.success(data=data)


async def update_userinfo(request: Request, username: str, obj: UpdateUser):
    """更新用户信息"""
    count = await UserService.update(request=request, username=username, obj=obj)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


async def update_user_avatar(request: Request, username: str, avatar: Avatar):
    """更新用户头像"""
    count = await UserService.update_avatar(request=request, username=username, avatar=avatar)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


async def get_all_users(
    db: CurrentSession,
    username: Annotated[str | None, Query()] = None,
    phone: Annotated[str | None, Query()] = None,
    status: Annotated[bool | None, Query()] = None,
):
    """（模糊条件）获取所有用户"""
    user_select = await UserService.get_select(username=username, phone=phone, status=status)
    page_data = await paging_data(db, user_select, GetAllUserInfo)
    return await response_base.success(data=page_data)


async def update_user_super(request: Request, pk: int):
    """更新用户超级管理员状态"""
    count = await UserService.update_permission(request=request, pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


async def update_user_active(request: Request, pk: int):
    """更新用户激活状态"""
    count = await UserService.update_active(request=request, pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


async def update_user_multi(request: Request, pk: int):
    """更新用户多点登录状态"""
    count = await UserService.update_multi_login(request=request, pk=pk)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


async def delete_user(request: Request, username: str):
    """删除用户"""
    count = await UserService.delete(request=request, username=username)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()
