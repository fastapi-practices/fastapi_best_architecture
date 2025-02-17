#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from backend.common.pagination import DependsPagination, PageData, paging_data
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db import CurrentSession
from backend.plugin.casbin.schema.casbin_rule import (
    CreatePolicyParam,
    CreateUserRoleParam,
    DeleteAllPoliciesParam,
    DeletePolicyParam,
    DeleteUserRoleParam,
    GetPolicyDetail,
    UpdatePoliciesParam,
    UpdatePolicyParam,
)
from backend.plugin.casbin.service.casbin_service import casbin_service

router = APIRouter()


@router.get(
    '',
    summary='（模糊条件）分页获取所有权限策略',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_pagination_casbin(
    db: CurrentSession,
    ptype: Annotated[str | None, Query(description='策略类型, p / g')] = None,
    sub: Annotated[str | None, Query(description='用户 uuid / 角色')] = None,
) -> ResponseSchemaModel[PageData[GetPolicyDetail]]:
    casbin_select = await casbin_service.get_casbin_list(ptype=ptype, sub=sub)
    page_data = await paging_data(db, casbin_select)
    return response_base.success(data=page_data)


@router.get('/policies', summary='获取所有P权限策略', dependencies=[DependsJwtAuth])
async def get_all_policies(
    role: Annotated[int | None, Query(description='角色ID')] = None,
) -> ResponseSchemaModel[list[list[str]]]:
    policies = await casbin_service.get_policy_list(role=role)
    return response_base.success(data=policies)


@router.post(
    '/policy',
    summary='添加P权限策略',
    dependencies=[
        Depends(RequestPermission('casbin:p:add')),
        DependsRBAC,
    ],
)
async def create_policy(p: CreatePolicyParam) -> ResponseSchemaModel[bool]:
    """
    p 策略:

    - 推荐添加基于角色的访问权限, 需配合添加 g 策略才能真正拥有访问权限，适合配置全局接口访问策略<br>
    **格式**: 角色 role + 访问路径 path + 访问方法 method

    - 如果添加基于用户的访问权限, 不需配合添加 g 策略就能真正拥有权限，适合配置指定用户接口访问策略<br>
    **格式**: 用户 uuid + 访问路径 path + 访问方法 method
    """
    data = await casbin_service.create_policy(p=p)
    return response_base.success(data=data)


@router.post(
    '/policies',
    summary='添加多组P权限策略',
    dependencies=[
        Depends(RequestPermission('casbin:p:group:add')),
        DependsRBAC,
    ],
)
async def create_policies(ps: list[CreatePolicyParam]) -> ResponseSchemaModel[bool]:
    data = await casbin_service.create_policies(ps=ps)
    return response_base.success(data=data)


@router.put(
    '/policy',
    summary='更新P权限策略',
    dependencies=[
        Depends(RequestPermission('casbin:p:edit')),
        DependsRBAC,
    ],
)
async def update_policy(obj: UpdatePolicyParam) -> ResponseSchemaModel[bool]:
    data = await casbin_service.update_policy(obj=obj)
    return response_base.success(data=data)


@router.put(
    '/policies',
    summary='更新多组P权限策略',
    dependencies=[
        Depends(RequestPermission('casbin:p:group:edit')),
        DependsRBAC,
    ],
)
async def update_policies(obj: UpdatePoliciesParam) -> ResponseSchemaModel[bool]:
    data = await casbin_service.update_policies(obj=obj)
    return response_base.success(data=data)


@router.delete(
    '/policy',
    summary='删除P权限策略',
    dependencies=[
        Depends(RequestPermission('casbin:p:del')),
        DependsRBAC,
    ],
)
async def delete_policy(p: DeletePolicyParam) -> ResponseSchemaModel[bool]:
    data = await casbin_service.delete_policy(p=p)
    return response_base.success(data=data)


@router.delete(
    '/policies',
    summary='删除多组P权限策略',
    dependencies=[
        Depends(RequestPermission('casbin:p:group:del')),
        DependsRBAC,
    ],
)
async def delete_policies(ps: list[DeletePolicyParam]) -> ResponseSchemaModel[bool]:
    data = await casbin_service.delete_policies(ps=ps)
    return response_base.success(data=data)


@router.delete(
    '/policies/all',
    summary='删除所有P权限策略',
    dependencies=[
        Depends(RequestPermission('casbin:p:empty')),
        DependsRBAC,
    ],
)
async def delete_all_policies(sub: DeleteAllPoliciesParam) -> ResponseModel:
    count = await casbin_service.delete_all_policies(sub=sub)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.get('/groups', summary='获取所有G权限策略', dependencies=[DependsJwtAuth])
async def get_all_groups() -> ResponseSchemaModel[list[list[str]]]:
    data = await casbin_service.get_group_list()
    return response_base.success(data=data)


@router.post(
    '/group',
    summary='添加G权限策略',
    dependencies=[
        Depends(RequestPermission('casbin:g:add')),
        DependsRBAC,
    ],
)
async def create_group(g: CreateUserRoleParam) -> ResponseSchemaModel[bool]:
    """
    g 策略 (**依赖 p 策略**):

    - 如果在 p 策略中添加了基于角色的访问权限, 则还需要在 g 策略中添加基于用户组的访问权限, 才能真正拥有访问权限<br>
    **格式**: 用户 uuid + 角色 role

    - 如果在 p 策略中添加了基于用户的访问权限, 则不添加相应的 g 策略能直接拥有访问权限<br>
    但是拥有的不是用户角色的所有权限, 而只是单一的对应的 p 策略所添加的访问权限
    """
    data = await casbin_service.create_group(g=g)
    return response_base.success(data=data)


@router.post(
    '/groups',
    summary='添加多组G权限策略',
    dependencies=[
        Depends(RequestPermission('casbin:g:group:add')),
        DependsRBAC,
    ],
)
async def create_groups(gs: list[CreateUserRoleParam]) -> ResponseSchemaModel[bool]:
    data = await casbin_service.create_groups(gs=gs)
    return response_base.success(data=data)


@router.delete(
    '/group',
    summary='删除G权限策略',
    dependencies=[
        Depends(RequestPermission('casbin:g:del')),
        DependsRBAC,
    ],
)
async def delete_group(g: DeleteUserRoleParam) -> ResponseSchemaModel[bool]:
    data = await casbin_service.delete_group(g=g)
    return response_base.success(data=data)


@router.delete(
    '/groups',
    summary='删除多组G权限策略',
    dependencies=[
        Depends(RequestPermission('casbin:g:group:del')),
        DependsRBAC,
    ],
)
async def delete_groups(gs: list[DeleteUserRoleParam]) -> ResponseSchemaModel[bool]:
    data = await casbin_service.delete_groups(gs=gs)
    return response_base.success(data=data)


@router.delete(
    '/groups/all',
    summary='删除所有G权限策略',
    dependencies=[
        Depends(RequestPermission('casbin:g:empty')),
        DependsRBAC,
    ],
)
async def delete_all_groups(uuid: Annotated[UUID, Query(...)]) -> ResponseModel:
    count = await casbin_service.delete_all_groups(uuid=uuid)
    if count > 0:
        return response_base.success()
    return response_base.fail()
