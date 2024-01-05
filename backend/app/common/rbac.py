#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import casbin

from casbin_async_redis_adapter.adapter import Adapter
from fastapi import Depends, Request

from backend.app.common.enums import StatusType
from backend.app.common.exception.errors import AuthorizationError, TokenError
from backend.app.common.jwt import jwt_auth
from backend.app.core.conf import settings


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
        adapter = Adapter(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.CASBIN_REDIS_DATABASE,
            password=settings.REDIS_PASSWORD,
        )
        model = casbin.AsyncEnforcer.new_model(text=_CASBIN_RBAC_MODEL_CONF_TEXT)
        enforcer = casbin.AsyncEnforcer(model, adapter)
        await enforcer.load_policy()
        return enforcer

    async def rbac_verify(self, request: Request, _token: str = Depends(jwt_auth)) -> None:
        """
        RBAC 权限校验

        :param request:
        :param _token:
        :return:
        """
        path = request.url.path
        if path in settings.TOKEN_EXCLUDE:
            return
        # 强制校验 JWT 授权状态
        if not request.auth.scopes:
            raise TokenError
        # 超级管理员免校验
        super_user = request.user.is_superuser
        if super_user:
            return
        # 检测角色数据权限范围
        user_roles = request.user.roles
        if not user_roles:
            raise AuthorizationError(msg='用户未分配角色，授权失败')
        if not any(len(role.menus) > 0 for role in user_roles):
            raise AuthorizationError(msg='用户所属角色未分配菜单，授权失败')
        if not request.user.is_staff:
            raise AuthorizationError(msg='此用户已被禁止后台管理操作')
        data_scope = any(role.data_scope == 1 for role in user_roles)
        if data_scope:
            return
        method = request.method
        # TODO: 手动编写每一个路由权限标识，使用 fastapi Depends 实现
        path_auth = 'todo'
        if settings.PERMISSION_MODE == 'role-menu':
            # 菜单权限校验
            if path_auth in set(settings.MENU_EXCLUDE):
                return
            menu_perms = []
            forbid_menu_perms = []
            for role in user_roles:
                user_menus = role.menus
                if user_menus:
                    for menu in user_menus:
                        perms = menu.perms
                        if menu.status == StatusType.enable:
                            menu_perms.extend(perms.split(','))
                        else:
                            forbid_menu_perms.extend(perms.split(','))
            if path_auth in set(forbid_menu_perms):
                raise AuthorizationError(msg='菜单已禁用，授权失败')
            if path_auth not in set(menu_perms):
                raise AuthorizationError
        else:
            # casbin 权限校验
            forbid_menu_path = []
            for role in user_roles:
                user_menus = role.menus
                if user_menus:
                    for menu in user_menus:
                        if menu.status == StatusType.disable:
                            forbid_menu_path.append(menu.perms)
            if path_auth in forbid_menu_path:
                raise AuthorizationError(msg='菜单已禁用，授权失败')
            if (method, path) in settings.CASBIN_EXCLUDE:
                return
            user_uuid = request.user.uuid
            enforcer = await self.enforcer()
            if not enforcer.enforce(user_uuid, path, method):
                raise AuthorizationError


RBAC = RBAC()
