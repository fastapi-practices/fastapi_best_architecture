#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import Depends, Request

from backend.common.enums import MethodType, StatusType
from backend.common.exception.errors import AuthorizationError, TokenError
from backend.common.security.jwt import DependsJwtAuth
from backend.core.conf import settings
from backend.plugin.casbin.utils.rbac import casbin_verify


async def rbac_verify(request: Request, _token: str = DependsJwtAuth) -> None:
    """
    RBAC 权限校验（鉴权顺序很重要，谨慎修改）

    :param request:
    :param _token:
    :return:
    """
    path = request.url.path

    # API 鉴权白名单
    if path in settings.TOKEN_REQUEST_PATH_EXCLUDE:
        return

    # JWT 授权状态强制校验
    if not request.auth.scopes:
        raise TokenError

    # 超级管理员免校验
    if request.user.is_superuser:
        return

    # 检测用户角色
    user_roles = request.user.roles
    if not user_roles or all(status == 0 for status in user_roles):
        raise AuthorizationError(msg='用户未分配角色，请联系系统管理员')

    # 检测用户所属角色菜单
    if not any(len(role.menus) > 0 for role in user_roles):
        raise AuthorizationError(msg='用户未分配菜单，请联系系统管理员')

    # 检测后台管理操作权限
    method = request.method
    if method != MethodType.GET or method != MethodType.OPTIONS:
        if not request.user.is_staff:
            raise AuthorizationError(msg='用户已被禁止后台管理操作，请联系系统管理员')

    # RBAC 鉴权
    if settings.RBAC_ROLE_MENU_MODE:
        path_auth_perm = getattr(request.state, 'permission', None)

        # 没有菜单操作权限标识不校验
        if not path_auth_perm:
            return

        # 菜单鉴权白名单
        if path_auth_perm in settings.RBAC_ROLE_MENU_EXCLUDE:
            return

        # 已分配菜单权限校验
        allow_perms = []
        for role in user_roles:
            for menu in role.menus:
                if menu.perms and menu.status == StatusType.enable:
                    allow_perms.extend(menu.perms.split(','))
        if path_auth_perm not in allow_perms:
            raise AuthorizationError
    else:
        await casbin_verify(request)


# RBAC 授权依赖注入
DependsRBAC = Depends(rbac_verify)
