#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query, Request

from backend.app.admin.schema.role import GetRoleDetail
from backend.app.admin.schema.user import (
    AddUserParam,
    GetCurrentUserInfoWithRelationDetail,
    GetUserInfoWithRelationDetail,
    ResetPasswordParam,
    UpdateUserParam,
)
from backend.app.admin.service.user_service import user_service
from backend.common.enums import UserPermissionType
from backend.common.pagination import DependsPagination, PageData, paging_data
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db import CurrentSession

router = APIRouter()


@router.get('/me', summary='获取当前用户信息', dependencies=[DependsJwtAuth])
async def get_current_user(request: Request) -> ResponseSchemaModel[GetCurrentUserInfoWithRelationDetail]:
    data = request.user.model_dump()
    return response_base.success(data=data)


@router.get('/{pk}', summary='获取用户信息', dependencies=[DependsJwtAuth])
async def get_userinfo(
    pk: Annotated[int, Path(description='用户 ID')],
) -> ResponseSchemaModel[GetUserInfoWithRelationDetail]:
    data = await user_service.get_userinfo(pk=pk)
    return response_base.success(data=data)


@router.get('/{pk}/roles', summary='获取用户所有角色', dependencies=[DependsJwtAuth])
async def get_user_roles(pk: Annotated[int, Path(description='用户 ID')]) -> ResponseSchemaModel[list[GetRoleDetail]]:
    data = await user_service.get_roles(pk=pk)
    return response_base.success(data=data)


@router.get(
    '',
    summary='分页获取所有用户',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_users_paged(
    db: CurrentSession,
    dept: Annotated[int | None, Query(description='部门 ID')] = None,
    username: Annotated[str | None, Query(description='用户名')] = None,
    phone: Annotated[str | None, Query(description='手机号')] = None,
    status: Annotated[int | None, Query(description='状态')] = None,
) -> ResponseSchemaModel[PageData[GetUserInfoWithRelationDetail]]:
    user_select = await user_service.get_select(dept=dept, username=username, phone=phone, status=status)
    page_data = await paging_data(db, user_select)
    return response_base.success(data=page_data)


@router.post('', summary='创建用户', dependencies=[DependsRBAC])
async def create_user(request: Request, obj: AddUserParam) -> ResponseSchemaModel[GetUserInfoWithRelationDetail]:
    await user_service.create(request=request, obj=obj)
    data = await user_service.get_userinfo(username=obj.username)
    return response_base.success(data=data)


@router.put('/{pk}', summary='更新用户信息', dependencies=[DependsRBAC])
async def update_user(
    request: Request, pk: Annotated[int, Path(description='用户 ID')], obj: UpdateUserParam
) -> ResponseModel:
    count = await user_service.update(request=request, pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.put('/{pk}/permissions', summary='更新用户权限', dependencies=[DependsRBAC])
async def update_user_permission(
    request: Request,
    pk: Annotated[int, Path(description='用户 ID')],
    type: Annotated[UserPermissionType, Query(description='权限类型')],
) -> ResponseModel:
    count = await user_service.update_permission(request=request, pk=pk, type=type)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.put('/me/password', summary='更新当前用户密码', dependencies=[DependsJwtAuth])
async def update_user_password(request: Request, obj: ResetPasswordParam) -> ResponseModel:
    count = await user_service.update_password(request=request, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.put('/{pk}/password', summary='重置用户密码', dependencies=[DependsRBAC])
async def reset_user_password(
    request: Request,
    pk: Annotated[int, Path(description='用户 ID')],
    password: Annotated[str, Body(embed=True, description='新密码')],
) -> ResponseModel:
    count = await user_service.reset_password(request=request, pk=pk, password=password)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.put('/me/nickname', summary='更新当前用户昵称', dependencies=[DependsJwtAuth])
async def update_user_nickname(
    request: Request, nickname: Annotated[str, Body(embed=True, description='用户昵称')]
) -> ResponseModel:
    count = await user_service.update_nickname(request=request, nickname=nickname)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.put('/me/avatar', summary='更新当前用户头像', dependencies=[DependsJwtAuth])
async def update_user_avatar(
    request: Request, avatar: Annotated[str, Body(embed=True, description='用户头像地址')]
) -> ResponseModel:
    count = await user_service.update_avatar(request=request, avatar=avatar)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    path='/{pk}',
    summary='删除用户',
    dependencies=[
        Depends(RequestPermission('sys:user:del')),
        DependsRBAC,
    ],
)
async def delete_user(pk: Annotated[int, Path(description='用户 ID')]) -> ResponseModel:
    count = await user_service.delete(pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()
