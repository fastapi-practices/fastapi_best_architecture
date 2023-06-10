#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.api.v1 import dept as dept_views
from backend.app.common.casbin_rbac import DependsRBAC
from backend.app.common.jwt import DependsJwtAuth

router = APIRouter()

router.add_api_route(
    path='/{pk}',
    endpoint=dept_views.get_dept,
    methods=['GET'],
    summary='获取部门详情',
    dependencies=[DependsJwtAuth],
)

router.add_api_route(
    path='',
    endpoint=dept_views.get_all_depts,
    methods=['GET'],
    summary='（模糊条件）获取所有部门展示树',
    dependencies=[DependsJwtAuth],
)

router.add_api_route(
    path='',
    endpoint=dept_views.create_dept,
    methods=['POST'],
    summary='创建部门',
    dependencies=[DependsRBAC],
)

router.add_api_route(
    path='/{pk}',
    endpoint=dept_views.update_dept,
    methods=['PUT'],
    summary='更新部门',
    dependencies=[DependsRBAC],
)

router.add_api_route(
    path='/{pk}',
    endpoint=dept_views.delete_dept,
    methods=['DELETE'],
    summary='删除部门',
    dependencies=[DependsRBAC],
)
