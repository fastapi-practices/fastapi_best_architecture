#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, Request

from backend.app.admin.schema.role import GetRoleDetail
from backend.app.admin.schema.user import (
    AddUserParam,
    GetCurrentUserInfoWithRelationDetail,
    GetUserInfoWithRelationDetail,
    ResetPasswordParam,
    UpdateUserParam,
)
from backend.app.admin.service.user_service import user_service
from backend.common.pagination import DependsPagination, PageData, paging_data
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db import CurrentSession

router = APIRouter()


@router.post('/add', summary='添加用户', dependencies=[DependsRBAC])
async def add_user(request: Request, obj: AddUserParam) -> ResponseSchemaModel[GetUserInfoWithRelationDetail]:
    await user_service.add(request=request, obj=obj)
    data = await user_service.get_userinfo(username=obj.username)
    return response_base.success(data=data)


@router.post('/{username}/password', summary='密码重置', dependencies=[DependsJwtAuth])
async def password_reset(
    username: Annotated[str, Path(description='用户名')], obj: ResetPasswordParam
) -> ResponseModel:
    count = await user_service.pwd_reset(username=username, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.get('/me', summary='获取当前用户信息', dependencies=[DependsJwtAuth])
async def get_current_user(request: Request) -> ResponseSchemaModel[GetCurrentUserInfoWithRelationDetail]:
    data = request.user.model_dump()
    return response_base.success(data=data)


@router.get('/{username}', summary='查看用户信息', dependencies=[DependsJwtAuth])
async def get_user(
    username: Annotated[str, Path(description='用户名')],
) -> ResponseSchemaModel[GetUserInfoWithRelationDetail]:
    data = await user_service.get_userinfo(username=username)
    return response_base.success(data=data)


@router.get('/{username}/roles', summary='获取用户所有角色', dependencies=[DependsJwtAuth])
async def get_user_all_roles(
    username: Annotated[str, Path(description='用户名')],
) -> ResponseSchemaModel[list[GetRoleDetail]]:
    data = await user_service.get_roles(username=username)
    return response_base.success(data=data)


@router.get(
    '',
    summary='分页获取所有用户',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_pagination_users(
    db: CurrentSession,
    dept: Annotated[int | None, Query(description='部门 ID')] = None,
    username: Annotated[str | None, Query(description='用户名')] = None,
    phone: Annotated[str | None, Query(description='手机号')] = None,
    status: Annotated[int | None, Query(description='状态')] = None,
) -> ResponseSchemaModel[PageData[GetUserInfoWithRelationDetail]]:
    user_select = await user_service.get_select(dept=dept, username=username, phone=phone, status=status)
    page_data = await paging_data(db, user_select)
    return response_base.success(data=page_data)


@router.put('/{username}', summary='更新用户信息', dependencies=[DependsJwtAuth])
async def update_user(
    request: Request, username: Annotated[str, Path(description='用户名')], obj: UpdateUserParam
) -> ResponseModel:
    count = await user_service.update(request=request, username=username, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.put('/{pk}/super', summary='修改用户超级权限', dependencies=[DependsRBAC])
async def super_set(request: Request, pk: Annotated[int, Path(description='用户 ID')]) -> ResponseModel:
    count = await user_service.update_permission(request=request, pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.put('/{pk}/staff', summary='修改用户后台登录权限', dependencies=[DependsRBAC])
async def staff_set(request: Request, pk: Annotated[int, Path(description='用户 ID')]) -> ResponseModel:
    count = await user_service.update_staff(request=request, pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.put('/{pk}/status', summary='修改用户状态', dependencies=[DependsRBAC])
async def status_set(request: Request, pk: Annotated[int, Path(description='用户 ID')]) -> ResponseModel:
    count = await user_service.update_status(request=request, pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.put('/{pk}/multi', summary='修改用户多端登录状态', dependencies=[DependsRBAC])
async def multi_set(request: Request, pk: Annotated[int, Path(description='用户 ID')]) -> ResponseModel:
    count = await user_service.update_multi_login(request=request, pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    path='/{username}',
    summary='删除用户',
    dependencies=[
        Depends(RequestPermission('sys:user:del')),
        DependsRBAC,
    ],
)
async def delete_user(username: Annotated[str, Path(description='用户名')]) -> ResponseModel:
    count = await user_service.delete(username=username)
    if count > 0:
        return response_base.success()
    return response_base.fail()
