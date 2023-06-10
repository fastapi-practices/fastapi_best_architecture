#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Query

from backend.app.common.casbin_rbac import DependsRBAC
from backend.app.common.pagination import paging_data
from backend.app.common.response.response_schema import response_base
from backend.app.database.db_mysql import CurrentSession
from backend.app.schemas.casbin_rule import (
    CreatePolicy,
    UpdatePolicy,
    DeletePolicy,
    CreateUserRole,
    DeleteUserRole,
    GetAllPolicy,
)
from backend.app.services.casbin_service import CasbinService

router = APIRouter()


async def get_all_casbin(
    db: CurrentSession,
    ptype: Annotated[str | None, Query()] = None,
    sub: Annotated[str | None, Query()] = None,
):
    """（模糊条件）分页获取所有casbin"""
    casbin_select = await CasbinService.get_casbin_list(ptype=ptype, sub=sub)
    page_data = await paging_data(db, casbin_select, GetAllPolicy)
    return await response_base.success(data=page_data)


async def get_all_policies():
    """获取所有 P 规则"""
    policies = await CasbinService.get_policy_list()
    return await response_base.success(data=policies)


async def create_policy(p: CreatePolicy):
    """
    添加基于角色(主)/用户(次)的访问权限

    p 规则:

    - 推荐添加基于角色的访问权限, 需配合添加 g 规则才能真正拥有访问权限，适合配置全局接口访问策略<br>
    **格式**: 角色 role + 访问路径 path + 访问方法 method

    - 如果添加基于用户的访问权限, 不需配合添加 g 规则就能真正拥有权限，适合配置指定用户接口访问策略<br>
    **格式**: 用户 uuid + 访问路径 path + 访问方法 method
    """
    data = await CasbinService.create_policy(p=p)
    return await response_base.success(data=data)


@router.put('/policy', summary='', dependencies=[DependsRBAC])
async def update_policy(old: UpdatePolicy, new: UpdatePolicy):
    """更新基于角色(主)/用户(次)的访问权限"""
    data = await CasbinService.update_policy(old=old, new=new)
    return await response_base.success(data=data)


async def delete_policy(p: DeletePolicy):
    """删除基于角色(主)/用户(次)的访问权限"""
    data = await CasbinService.delete_policy(p=p)
    return await response_base.success(data=data)


async def get_all_grouping_policies():
    """获取所有 g 规则"""
    data = await CasbinService.get_group_list()
    return await response_base.success(data=data)


async def create_grouping_policy(g: CreateUserRole):
    """
    添加基于用户组的访问权限

    g 规则 (**依赖 p 规则**):

    - 如果在 p 规则中添加了基于角色的访问权限, 则还需要在 g 规则中添加基于用户组的访问权限, 才能真正拥有访问权限<br>
    **格式**: 用户 uuid + 角色 role

    - 如果在p策略中添加了基于用户的访问权限, 则不添加相应的 g 规则能直接拥有访问权限<br>
    但是拥有的不是用户角色的所有权限, 而只是单一的对应的 p 规则所添加的访问权限
    """
    data = await CasbinService.create_group(g=g)
    return await response_base.success(data=data)


async def delete_grouping_policy(g: DeleteUserRole):
    """删除基于用户组的访问权限"""
    data = await CasbinService.delete_group(g=g)
    return await response_base.success(data=data)
