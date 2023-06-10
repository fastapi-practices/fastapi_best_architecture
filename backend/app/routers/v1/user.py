#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.app.api.v1 import user as user_views
from backend.app.common.jwt import DependsJwtAuth

router = APIRouter()

router.add_api_route(
    path='/register',
    endpoint=user_views.register_user,
    methods=['POST'],
    summary='注册用户',
)

router.add_api_route(
    path='/password/reset',
    endpoint=user_views.reset_password,
    methods=['POST'],
    summary='重置密码',
    dependencies=[DependsJwtAuth],
)

router.add_api_route(
    path='/{username}',
    endpoint=user_views.get_user,
    methods=['GET'],
    summary='获取用户详情',
    dependencies=[DependsJwtAuth],
)

router.add_api_route(
    path='/{username}',
    endpoint=user_views.update_userinfo,
    methods=['PUT'],
    summary='更新用户信息',
    dependencies=[DependsJwtAuth],
)

router.add_api_route(
    path='/{username}/avatar',
    endpoint=user_views.update_user_avatar,
    methods=['PUT'],
    summary='更新用户头像',
    dependencies=[DependsJwtAuth],
)

router.add_api_route(
    path='',
    endpoint=user_views.get_all_users,
    methods=['GET'],
    summary='（模糊条件）分页获取所有用户',
    dependencies=[DependsJwtAuth],
)

router.add_api_route(
    path='/{pk}/super',
    endpoint=user_views.update_user_super,
    methods=['PUT'],
    summary='更新用户超级管理员状态',
    dependencies=[DependsJwtAuth],
)

router.add_api_route(
    path='/{pk}/status',
    endpoint=user_views.update_user_active,
    methods=['PUT'],
    summary='更新用户激活状态',
    dependencies=[DependsJwtAuth],
)

router.add_api_route(
    path='/{pk}/multi',
    endpoint=user_views.update_user_multi,
    methods=['PUT'],
    summary='更新用户多点登录状态',
    dependencies=[DependsJwtAuth],
)

router.add_api_route(
    path='/{username}',
    endpoint=user_views.delete_user,
    methods=['DELETE'],
    summary='用户注销',
    description='用户注销 != 用户登出，注销之后用户将从数据库删除',
    dependencies=[DependsJwtAuth],
)
