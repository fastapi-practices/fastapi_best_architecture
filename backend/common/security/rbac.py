#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import casbin
import casbin_async_sqlalchemy_adapter

from fastapi import Depends, Request

from backend.app.admin.model import CasbinRule
from backend.common.enums import MethodType, StatusType
from backend.common.exception.errors import AuthorizationError, TokenError
from backend.common.security.jwt import DependsJwtAuth
from backend.core.conf import settings
from backend.database.db_mysql import async_engine


class RBAC:
    @staticmethod
    async def enforcer() -> casbin.AsyncEnforcer:
        """
        获取 casbin 执行器

        :return:
        """
        # 规则数据作为死数据直接在方法内定义
        _CASBIN_RBAC_MODEL_CONF_TEXT = """
        [request_definition]
        r = sub, obj, act

        [policy_definition]
        p = sub, obj, act

        [role_definition]
        g = _, _

        [policy_effect]
        e = some(where (p.eft == allow))

        [matchers]
        m = g(r.sub, p.sub) && (keyMatch(r.obj, p.obj) || keyMatch3(r.obj, p.obj)) && (r.act == p.act || p.act == "*")
        """
        adapter = casbin_async_sqlalchemy_adapter.Adapter(async_engine, db_class=CasbinRule)
        model = casbin.AsyncEnforcer.new_model(text=_CASBIN_RBAC_MODEL_CONF_TEXT)
        enforcer = casbin.AsyncEnforcer(model, adapter)
        await enforcer.load_policy()
        return enforcer

    async def rbac_verify(self, request: Request, _token: str = DependsJwtAuth) -> None:
        """
        RBAC 权限校验

        :param request:
        :param _token:
        :return:
        """
        path = request.url.path
        # 鉴权白名单
        if path in settings.TOKEN_REQUEST_PATH_EXCLUDE:
            return
        # JWT 授权状态强制校验
        if not request.auth.scopes:
            raise TokenError
        # 超级管理员免校验
        if request.user.is_superuser:
            return
        # 检测角色数据权限范围
        user_roles = request.user.roles
        if not user_roles:
            raise AuthorizationError(msg='用户未分配角色，授权失败')
        if not any(len(role.menus) > 0 for role in user_roles):
            raise AuthorizationError(msg='用户所属角色未分配菜单，授权失败')
        method = request.method
        if method != MethodType.GET or method != MethodType.OPTIONS:
            if not request.user.is_staff:
                raise AuthorizationError(msg='此用户已被禁止后台管理操作')
        # 数据权限范围
        data_scope = any(role.data_scope == 1 for role in user_roles)
        if data_scope:
            return
        user_uuid = request.user.uuid
        if settings.PERMISSION_MODE == 'role-menu':
            # 角色菜单权限校验
            path_auth_perm = getattr(request.state, 'permission', None)
            # 没有菜单权限标识不校验
            if not path_auth_perm:
                return
            if path_auth_perm in set(settings.RBAC_ROLE_MENU_EXCLUDE):
                return
            allow_perms = []
            for role in user_roles:
                for menu in role.menus:
                    if menu.status == StatusType.enable:
                        allow_perms.extend(menu.perms.split(','))
            if path_auth_perm not in allow_perms:
                raise AuthorizationError
        else:
            # casbin 权限校验
            if (method, path) in settings.RBAC_CASBIN_EXCLUDE:
                return
            enforcer = await self.enforcer()
            if not enforcer.enforce(user_uuid, path, method):
                raise AuthorizationError


rbac = RBAC()
# RBAC 授权依赖注入
DependsRBAC = Depends(rbac.rbac_verify)
