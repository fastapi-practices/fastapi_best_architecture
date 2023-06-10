#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.api.v1 import api as api_views
from backend.app.common.casbin_rbac import DependsRBAC
from backend.app.common.jwt import DependsJwtAuth
from backend.app.common.pagination import PageDepends

router = APIRouter()

router.add_api_route(
    path='/{pk}',
    endpoint=api_views.get_api,
    methods=['GET'],
    summary='获取接口详情',
    dependencies=[DependsJwtAuth],
)

router.add_api_route(
    path='',
    endpoint=api_views.get_all_apis,
    methods=['GET'],
    summary='（模糊条件）分页获取所有接口',
    dependencies=[DependsJwtAuth, PageDepends],
)

router.add_api_route(
    path='',
    endpoint=api_views.create_api,
    methods=['POST'],
    summary='创建接口',
    dependencies=[DependsRBAC],
)

router.add_api_route(
    path='/{pk}',
    endpoint=api_views.update_api,
    methods=['PUT'],
    summary='更新接口',
    dependencies=[DependsRBAC],
)

router.add_api_route(
    path='',
    endpoint=api_views.delete_api,
    methods=['DELETE'],
    summary='（批量）删除接口',
    dependencies=[DependsRBAC],
)
