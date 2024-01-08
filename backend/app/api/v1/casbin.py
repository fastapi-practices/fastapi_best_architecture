#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from backend.app.common.jwt import DependsJwtAuth
from backend.app.common.pagination import DependsPagination, paging_data
from backend.app.common.permission import RequestPermission
from backend.app.common.rbac import DependsRBAC
from backend.app.common.response.response_schema import response_base
from backend.app.database.db_mysql import CurrentSession
from backend.app.schemas.casbin_rule import (
    CreatePolicy,
    CreateUserRole,
    DeleteAllPolicies,
    DeletePolicy,
    DeleteUserRole,
    GetAllPolicy,
    UpdatePolicy,
)
from backend.app.services.casbin_service import CasbinService

router = APIRouter()


@router.get(
    '',
    summary='（模糊条件）分页获取所有权限规则',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_all_casbin(
    db: CurrentSession,
    ptype: Annotated[str | None, Query(description='规则类型, p / g')] = None,
    sub: Annotated[str | None, Query(description='用户 uuid / 角色')] = None,
):
    casbin_select = await CasbinService.get_casbin_list(ptype=ptype, sub=sub)
    page_data = await paging_data(db, casbin_select, GetAllPolicy)
    return await response_base.success(data=page_data)


@router.get('/policy', summary='获取所有P权限规则', dependencies=[DependsJwtAuth])
async def get_all_policies():
    policies = await CasbinService.get_policy_list()
    return await response_base.success(data=policies)


@router.get('/policy/{role}/all', summary='获取指定角色的所有P权限规则', dependencies=[DependsJwtAuth])
async def get_role_policies(role: Annotated[str, Path(description='角色ID')]):
    policies = await CasbinService.get_policy_list_by_role(role=role)
    return await response_base.success(data=policies)


@router.post(
    '/policy',
    summary='添加P权限规则',
    dependencies=[
        Depends(RequestPermission('casbin:p:add')),
        DependsRBAC,
    ],
)
async def create_policy(p: CreatePolicy):
    """
    p 规则:

    - 推荐添加基于角色的访问权限, 需配合添加 g 规则才能真正拥有访问权限，适合配置全局接口访问策略<br>
    **格式**: 角色 role + 访问路径 path + 访问方法 method

    - 如果添加基于用户的访问权限, 不需配合添加 g 规则就能真正拥有权限，适合配置指定用户接口访问策略<br>
    **格式**: 用户 uuid + 访问路径 path + 访问方法 method
    """
    data = await CasbinService.create_policy(p=p)
    return await response_base.success(data=data)


@router.post(
    '/policies',
    summary='添加多组P权限规则',
    dependencies=[
        Depends(RequestPermission('casbin:p:group:add')),
        DependsRBAC,
    ],
)
async def create_policies(ps: list[CreatePolicy]):
    data = await CasbinService.create_policies(ps=ps)
    return await response_base.success(data=data)


@router.put(
    '/policy',
    summary='更新P权限规则',
    dependencies=[
        Depends(RequestPermission('casbin:p:edit')),
        DependsRBAC,
    ],
)
async def update_policy(old: UpdatePolicy, new: UpdatePolicy):
    data = await CasbinService.update_policy(old=old, new=new)
    return await response_base.success(data=data)


@router.put(
    '/policies',
    summary='更新多组P权限规则',
    dependencies=[
        Depends(RequestPermission('casbin:p:group:edit')),
        DependsRBAC,
    ],
)
async def update_policies(old: list[UpdatePolicy], new: list[UpdatePolicy]):
    data = await CasbinService.update_policies(old=old, new=new)
    return await response_base.success(data=data)


@router.delete(
    '/policy',
    summary='删除P权限规则',
    dependencies=[
        Depends(RequestPermission('casbin:p:del')),
        DependsRBAC,
    ],
)
async def delete_policy(p: DeletePolicy):
    data = await CasbinService.delete_policy(p=p)
    return await response_base.success(data=data)


@router.delete(
    '/policies',
    summary='删除多组P权限规则',
    dependencies=[
        Depends(RequestPermission('casbin:p:group:del')),
        DependsRBAC,
    ],
)
async def delete_policies(ps: list[DeletePolicy]):
    data = await CasbinService.delete_policies(ps=ps)
    return await response_base.success(data=data)


@router.delete(
    '/policies/all',
    summary='删除所有P权限规则',
    dependencies=[
        Depends(RequestPermission('casbin:p:empty')),
        DependsRBAC,
    ],
)
async def delete_all_policies(sub: DeleteAllPolicies):
    count = await CasbinService.delete_all_policies(sub=sub)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()


@router.get('/group', summary='获取所有G权限规则', dependencies=[DependsJwtAuth])
async def get_all_groups():
    data = await CasbinService.get_group_list()
    return await response_base.success(data=data)


@router.post(
    '/group',
    summary='添加G权限规则',
    dependencies=[
        Depends(RequestPermission('casbin:g:add')),
        DependsRBAC,
    ],
)
async def create_group(g: CreateUserRole):
    """
    g 规则 (**依赖 p 规则**):

    - 如果在 p 规则中添加了基于角色的访问权限, 则还需要在 g 规则中添加基于用户组的访问权限, 才能真正拥有访问权限<br>
    **格式**: 用户 uuid + 角色 role

    - 如果在 p 策略中添加了基于用户的访问权限, 则不添加相应的 g 规则能直接拥有访问权限<br>
    但是拥有的不是用户角色的所有权限, 而只是单一的对应的 p 规则所添加的访问权限
    """
    data = await CasbinService.create_group(g=g)
    return await response_base.success(data=data)


@router.post(
    '/groups',
    summary='添加多组G权限规则',
    dependencies=[
        Depends(RequestPermission('casbin:g:group:add')),
        DependsRBAC,
    ],
)
async def create_groups(gs: list[CreateUserRole]):
    data = await CasbinService.create_groups(gs=gs)
    return await response_base.success(data=data)


@router.delete(
    '/group',
    summary='删除G权限规则',
    dependencies=[
        Depends(RequestPermission('casbin:g:del')),
        DependsRBAC,
    ],
)
async def delete_group(g: DeleteUserRole):
    data = await CasbinService.delete_group(g=g)
    return await response_base.success(data=data)


@router.delete(
    '/groups',
    summary='删除多组G权限规则',
    dependencies=[
        Depends(RequestPermission('casbin:g:group:del')),
        DependsRBAC,
    ],
)
async def delete_groups(gs: list[DeleteUserRole]):
    data = await CasbinService.delete_groups(gs=gs)
    return await response_base.success(data=data)


@router.delete(
    '/groups/all',
    summary='删除所有G权限规则',
    dependencies=[
        Depends(RequestPermission('casbin:g:empty')),
        DependsRBAC,
    ],
)
async def delete_all_groups(uuid: str):
    count = await CasbinService.delete_all_groups(uuid=uuid)
    if count > 0:
        return await response_base.success()
    return await response_base.fail()
