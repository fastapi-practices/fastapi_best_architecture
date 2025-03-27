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
    CreateGroupParam,
    CreatePolicyParam,
    DeleteAllPoliciesParam,
    DeleteGroupParam,
    DeletePolicyParam,
    GetPolicyDetail,
    UpdatePoliciesParam,
    UpdatePolicyParam,
)
from backend.plugin.casbin.service.casbin_service import casbin_service

router = APIRouter()


@router.get(
    '',
    summary='分页获取所有权限策略',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_pagination_casbin(
    db: CurrentSession,
    ptype: Annotated[str | None, Query(description='策略类型：p / g')] = None,
    sub: Annotated[str | None, Query(description='用户 UUID / 角色 ID')] = None,
) -> ResponseSchemaModel[PageData[GetPolicyDetail]]:
    casbin_select = await casbin_service.get_casbin_list(ptype=ptype, sub=sub)
    page_data = await paging_data(db, casbin_select)
    return response_base.success(data=page_data)


@router.get('/policies', summary='获取所有 P 权限策略', dependencies=[DependsJwtAuth])
async def get_all_policies(
    role: Annotated[int | None, Query(description='角色 ID')] = None,
) -> ResponseSchemaModel[list[list[str]]]:
    policies = await casbin_service.get_policy_list(role=role)
    return response_base.success(data=policies)


@router.post(
    '/policy',
    summary='添加 P 权限策略',
    dependencies=[
        Depends(RequestPermission('casbin:p:add')),
        DependsRBAC,
    ],
)
async def create_policy(p: CreatePolicyParam) -> ResponseSchemaModel[bool]:
    data = await casbin_service.create_policy(p=p)
    return response_base.success(data=data)


@router.post(
    '/policies',
    summary='添加多组 P 权限策略',
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
    summary='更新 P 权限策略',
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
    summary='更新多组 P 权限策略',
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
    summary='删除 P 权限策略',
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
    summary='删除多组 P 权限策略',
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
    summary='删除所有 P 权限策略',
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


@router.get('/groups', summary='获取所有 G 权限策略', dependencies=[DependsJwtAuth])
async def get_all_groups() -> ResponseSchemaModel[list[list[str]]]:
    data = await casbin_service.get_group_list()
    return response_base.success(data=data)


@router.post(
    '/group',
    summary='添加 G 权限策略',
    dependencies=[
        Depends(RequestPermission('casbin:g:add')),
        DependsRBAC,
    ],
)
async def create_group(g: CreateGroupParam) -> ResponseSchemaModel[bool]:
    data = await casbin_service.create_group(g=g)
    return response_base.success(data=data)


@router.post(
    '/groups',
    summary='添加多组 G 权限策略',
    dependencies=[
        Depends(RequestPermission('casbin:g:group:add')),
        DependsRBAC,
    ],
)
async def create_groups(gs: list[CreateGroupParam]) -> ResponseSchemaModel[bool]:
    data = await casbin_service.create_groups(gs=gs)
    return response_base.success(data=data)


@router.delete(
    '/group',
    summary='删除 G 权限策略',
    dependencies=[
        Depends(RequestPermission('casbin:g:del')),
        DependsRBAC,
    ],
)
async def delete_group(g: DeleteGroupParam) -> ResponseSchemaModel[bool]:
    data = await casbin_service.delete_group(g=g)
    return response_base.success(data=data)


@router.delete(
    '/groups',
    summary='删除多组 G 权限策略',
    dependencies=[
        Depends(RequestPermission('casbin:g:group:del')),
        DependsRBAC,
    ],
)
async def delete_groups(gs: list[DeleteGroupParam]) -> ResponseSchemaModel[bool]:
    data = await casbin_service.delete_groups(gs=gs)
    return response_base.success(data=data)


@router.delete(
    '/groups/all',
    summary='删除所有 G 权限策略',
    dependencies=[
        Depends(RequestPermission('casbin:g:empty')),
        DependsRBAC,
    ],
)
async def delete_all_groups(uuid: Annotated[UUID, Query()]) -> ResponseModel:
    count = await casbin_service.delete_all_groups(uuid=uuid)
    if count > 0:
        return response_base.success()
    return response_base.fail()
