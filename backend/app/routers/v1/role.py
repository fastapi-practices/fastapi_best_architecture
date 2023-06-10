#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.api.v1 import role as role_views
from backend.app.common.casbin_rbac import DependsRBAC
from backend.app.common.jwt import DependsJwtAuth
from backend.app.common.pagination import PageDepends

router = APIRouter()

router.add_api_route(
    path='/{pk}',
    endpoint=role_views.get_role,
    methods=['GET'],
    summary='获取角色详情',
    dependencies=[DependsJwtAuth],
)

router.add_api_route(
    path='',
    endpoint=role_views.get_all_roles,
    methods=['GET'],
    summary='（模糊条件）分页获取所有角色',
    dependencies=[DependsJwtAuth, PageDepends],
)

router.add_api_route(
    path='',
    endpoint=role_views.create_role,
    methods=['POST'],
    summary='创建角色',
    dependencies=[DependsRBAC],
)

router.add_api_route(
    path='/{pk}',
    endpoint=role_views.update_role,
    methods=['PUT'],
    summary='更新角色',
    dependencies=[DependsRBAC],
)

router.add_api_route(
    path='',
    endpoint=role_views.delete_role,
    methods=['DELETE'],
    summary='（批量）删除角色',
    dependencies=[DependsRBAC],
)
