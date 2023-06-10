#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.api.v1 import login_log as login_log_views
from backend.app.common.casbin_rbac import DependsRBAC
from backend.app.common.jwt import DependsJwtAuth
from backend.app.common.pagination import PageDepends

router = APIRouter()

router.add_api_route(
    path='',
    endpoint=login_log_views.get_all_login_logs,
    methods=['GET'],
    summary='（模糊条件）分页获取登录日志',
    dependencies=[DependsJwtAuth, PageDepends],
)

router.add_api_route(
    path='',
    endpoint=login_log_views.delete_login_log,
    methods=['DELETE'],
    summary='（批量）删除登录日志',
    dependencies=[DependsRBAC],
)

router.add_api_route(
    path='/all',
    endpoint=login_log_views.delete_all_login_logs,
    methods=['DELETE'],
    summary='清空登录日志',
    dependencies=[DependsRBAC],
)
