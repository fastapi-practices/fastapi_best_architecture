#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.api.v1 import casbin as casbin_views
from backend.app.common.casbin_rbac import DependsRBAC
from backend.app.common.jwt import DependsJwtAuth
from backend.app.common.pagination import PageDepends

router = APIRouter()


router.add_api_route(
    path='',
    endpoint=casbin_views.get_all_casbin,
    methods=['GET'],
    summary='（模糊条件）分页获取所有casbin',
    dependencies=[DependsJwtAuth, PageDepends],
)

router.add_api_route(
    path='/policies',
    endpoint=casbin_views.get_all_policies,
    methods=['GET'],
    summary='获取所有 P 规则',
    dependencies=[DependsJwtAuth],
)

router.add_api_route(
    path='/policy',
    endpoint=casbin_views.create_policy,
    methods=['POST'],
    summary='添加基于角色(主)/用户(次)的访问权限',
    dependencies=[DependsRBAC],
)

router.add_api_route(
    path='/policy',
    endpoint=casbin_views.update_policy,
    methods=['PUT'],
    summary='更新基于角色(主)/用户(次)的访问权限',
    dependencies=[DependsRBAC],
)

router.add_api_route(
    path='/policy',
    endpoint=casbin_views.delete_policy,
    methods=['DELETE'],
    summary='删除基于角色(主)/用户(次)的访问权限',
    dependencies=[DependsRBAC],
)

router.add_api_route(
    path='/grouping_policies',
    endpoint=casbin_views.get_all_grouping_policies,
    methods=['GET'],
    summary='获取所有 G 规则',
    dependencies=[DependsJwtAuth],
)

router.add_api_route(
    path='/grouping_policy',
    endpoint=casbin_views.create_grouping_policy,
    methods=['POST'],
    summary='添加基于用户组的访问权限',
    dependencies=[DependsRBAC],
)

router.add_api_route(
    path='/grouping_policy',
    endpoint=casbin_views.delete_grouping_policy,
    methods=['DELETE'],
    summary='删除基于用户组的访问权限',
    dependencies=[DependsRBAC],
)
