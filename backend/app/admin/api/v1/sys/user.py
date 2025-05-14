#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, Request

from backend.app.admin.schema.user import (
    AddUserParam,
    AvatarParam,
    GetCurrentUserInfoWithRelationDetail,
    GetUserInfoWithRelationDetail,
    RegisterUserParam,
    ResetPasswordParam,
    UpdateUserParam,
    UpdateUserRoleParam,
)
from backend.app.admin.service.user_service import user_service
from backend.common.pagination import DependsPagination, PageData, paging_data
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db import CurrentSession

router = APIRouter()


@router.post('/register', summary='Registered users')
async def register_user(obj: RegisterUserParam) -> ResponseModel:
    await user_service.register(obj=obj)
    return response_base.success()


@router.post('/add', summary='Add User', dependencies=[DependsRBAC])
async def add_user(request: Request, obj: AddUserParam) -> ResponseSchemaModel[GetUserInfoWithRelationDetail]:
    await user_service.add(request=request, obj=obj)
    data = await user_service.get_userinfo(username=obj.username)
    return response_base.success(data=data)


@router.post('/password/reset', summary='Password Reset', dependencies=[DependsJwtAuth])
async def password_reset(request: Request, obj: ResetPasswordParam) -> ResponseModel:
    count = await user_service.pwd_reset(request=request, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.get('/me', summary='Get Current User Information', dependencies=[DependsJwtAuth])
async def get_current_user(request: Request) -> ResponseSchemaModel[GetCurrentUserInfoWithRelationDetail]:
    data = request.user.model_dump()
    return response_base.success(data=data)


@router.get('/{username}', summary='View User Information', dependencies=[DependsJwtAuth])
async def get_user(
    username: Annotated[str, Path(description='Username')],
) -> ResponseSchemaModel[GetUserInfoWithRelationDetail]:
    data = await user_service.get_userinfo(username=username)
    return response_base.success(data=data)


@router.put('/{username}', summary='Update user information', dependencies=[DependsJwtAuth])
async def update_user(
    request: Request, username: Annotated[str, Path(description='Username')], obj: UpdateUserParam
) -> ResponseModel:
    count = await user_service.update(request=request, username=username, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.put(
    '/{username}/role',
    summary='Update user roles',
    dependencies=[
        Depends(RequestPermission('sys:user:role:edit')),
        DependsRBAC,
    ],
)
async def update_user_role(
    request: Request, username: Annotated[str, Path(description='Username')], obj: UpdateUserRoleParam
) -> ResponseModel:
    await user_service.update_roles(request=request, username=username, obj=obj)
    return response_base.success()


@router.put('/{username}/avatar', summary='Update header', dependencies=[DependsJwtAuth])
async def update_avatar(
    request: Request, username: Annotated[str, Path(description='Username')], avatar: AvatarParam
) -> ResponseModel:
    count = await user_service.update_avatar(request=request, username=username, avatar=avatar)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.get(
    '',
    summary='Page Break All Users',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_pagination_users(
    db: CurrentSession,
    dept: Annotated[int | None, Query(description='SECTOR ID')] = None,
    username: Annotated[str | None, Query(description='Username')] = None,
    phone: Annotated[str | None, Query(description='Cell phone number')] = None,
    status: Annotated[int | None, Query(description='Status')] = None,
) -> ResponseSchemaModel[PageData[GetUserInfoWithRelationDetail]]:
    user_select = await user_service.get_select(dept=dept, username=username, phone=phone, status=status)
    page_data = await paging_data(db, user_select)
    return response_base.success(data=page_data)


@router.put('/{pk}/super', summary='Modify user super permissions', dependencies=[DependsRBAC])
async def super_set(request: Request, pk: Annotated[int, Path(description='USER ID')]) -> ResponseModel:
    count = await user_service.update_permission(request=request, pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.put('/{pk}/staff', summary='Modify user backstage login privileges', dependencies=[DependsRBAC])
async def staff_set(request: Request, pk: Annotated[int, Path(description='USER ID')]) -> ResponseModel:
    count = await user_service.update_staff(request=request, pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.put('/{pk}/status', summary='Modify User Status', dependencies=[DependsRBAC])
async def status_set(request: Request, pk: Annotated[int, Path(description='USER ID')]) -> ResponseModel:
    count = await user_service.update_status(request=request, pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.put('/{pk}/multi', summary='Modify user multi-end login status', dependencies=[DependsRBAC])
async def multi_set(request: Request, pk: Annotated[int, Path(description='USER ID')]) -> ResponseModel:
    count = await user_service.update_multi_login(request=request, pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    path='/{username}',
    summary='User write-off',
    description='User cancel! = User log-out, after write-off will be deleted from the database',
    dependencies=[
        Depends(RequestPermission('sys:user:del')),
        DependsRBAC,
    ],
)
async def delete_user(username: Annotated[str, Path(description='Username')]) -> ResponseModel:
    count = await user_service.delete(username=username)
    if count > 0:
        return response_base.success()
    return response_base.fail()
