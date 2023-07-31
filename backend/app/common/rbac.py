#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import casbin
import casbin_async_sqlalchemy_adapter
from fastapi import Request, Depends

from backend.app.common.enums import StatusType
from backend.app.common.exception.errors import AuthorizationError, TokenError
from backend.app.common.jwt import DependsJwtAuth
from backend.app.core.conf import settings
from backend.app.core.path_conf import RBAC_MODEL_CONF
from backend.app.database.db_mysql import async_engine
from backend.app.models.sys_casbin_rule import CasbinRule


class RBAC:
    @staticmethod
    async def enforcer() -> casbin.Enforcer:
        """
        获取 casbin 执行器

        :return:
        """
        adapter = casbin_async_sqlalchemy_adapter.Adapter(async_engine, db_class=CasbinRule)
        enforcer = casbin.Enforcer(RBAC_MODEL_CONF, adapter)
        await enforcer.load_policy()
        return enforcer

    async def rbac_verify(self, request: Request, _: dict = DependsJwtAuth) -> None:
        """
        RBAC 权限校验

        :param request:
        :param _:
        :return:
        """
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
        if settings.MENU_PERMISSION:
            # 菜单权限校验
            path_auth = request.url.path.replace(f'{settings.API_V1_STR}', '').replace('/', ':')
            menu_perms = []
            forbid_menu_perms = []
            for role in user_roles:
                for menu in role.menus:
                    menu_perms.append(menu.perms) if menu.status == StatusType.enable else forbid_menu_perms.append(
                        menu.perms
                    )
            if path_auth in set(settings.MENU_EXCLUDE):
                return
            if path_auth in set([perm for perms_str in forbid_menu_perms for perm in perms_str.split(',')]):
                raise AuthorizationError(msg='菜单已禁用，授权失败')
            if path_auth not in set([perm for perms_str in menu_perms for perm in perms_str.split(',')]):
                raise AuthorizationError
        else:
            # casbin 权限校验
            method = request.method
            path = request.url.path
            forbid_menu_path = [
                menu.path for role in user_roles for menu in role.menus if menu.status == StatusType.disable
            ]
            if path.split('/')[-1] in forbid_menu_path:
                raise AuthorizationError(msg='菜单已禁用，授权失败')
            if (method, path) in settings.CASBIN_EXCLUDE:
                return
            user_uuid = request.user.uuid
            enforcer = await self.enforcer()
            if not enforcer.enforce(user_uuid, path, method):
                raise AuthorizationError


RBAC = RBAC()
# RBAC 授权依赖注入
DependsRBAC = Depends(RBAC.rbac_verify)
