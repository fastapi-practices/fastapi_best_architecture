#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.api.v1 import opera_log as opera_log_views
from backend.app.common.casbin_rbac import DependsRBAC
from backend.app.common.jwt import DependsJwtAuth
from backend.app.common.pagination import PageDepends

router = APIRouter()

router.add_api_route(
    path='',
    endpoint=opera_log_views.get_all_opera_logs,
    methods=['GET'],
    summary='（模糊条件）分页获取操作日志',
    dependencies=[DependsJwtAuth, PageDepends],
)

router.add_api_route(
    path='',
    endpoint=opera_log_views.delete_opera_log,
    methods=['DELETE'],
    summary='（批量）删除操作日志',
    dependencies=[DependsRBAC],
)

router.add_api_route(
    path='/all',
    endpoint=opera_log_views.delete_all_opera_logs,
    methods=['DELETE'],
    summary='清空操作日志',
    dependencies=[DependsRBAC],
)
