#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from backend.app.api.v1.auth import auth as auth_views
from backend.app.common.jwt import DependsJwtAuth

router = APIRouter()

router.add_api_route(
    path='/swagger_login',
    endpoint=auth_views.swagger_user_login,
    methods=['POST'],
    summary='swagger 表单登录',
    description='form 格式登录，仅用于 swagger 文档调试接口',
)

router.add_api_route(
    path='/login',
    endpoint=auth_views.user_login,
    methods=['POST'],
    summary='用户登录',
    dependencies=[Depends(RateLimiter(times=5, minutes=15))],
)

router.add_api_route(
    path='/new_token',
    endpoint=auth_views.create_new_token,
    methods=['POST'],
    summary='创建新 token',
    dependencies=[DependsJwtAuth],
)

router.add_api_route(
    path='/logout',
    endpoint=auth_views.user_logout,
    methods=['POST'],
    summary='用户登出',
    dependencies=[DependsJwtAuth],
)
