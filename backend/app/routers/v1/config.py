#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.api.v1 import config as config_views
from backend.app.common.casbin_rbac import DependsRBAC

router = APIRouter()

router.add_api_route(
    path='', endpoint=config_views.get_sys_config, methods=['GET'], summary='获取系统配置详情', dependencies=[DependsRBAC]
)


router.add_api_route(
    path='/routers',
    endpoint=config_views.get_all_routers,
    methods=['GET'],
    summary='获取所有路由',
    dependencies=[DependsRBAC],
)
