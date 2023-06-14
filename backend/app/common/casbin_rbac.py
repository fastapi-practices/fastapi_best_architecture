#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import casbin
import casbin_async_sqlalchemy_adapter
from fastapi import Request, Depends

from backend.app.common.exception.errors import AuthorizationError, TokenError
from backend.app.common.jwt import oauth2_schema
from backend.app.core.conf import settings
from backend.app.core.path_conf import RBAC_MODEL_CONF
from backend.app.database.db_mysql import async_engine
from backend.app.models.sys_casbin_rule import CasbinRule


class RBAC:
    @staticmethod
    def enforcer() -> casbin.Enforcer:
        """
        获取 casbin 执行器

        :return:
        """
        adapter = casbin_async_sqlalchemy_adapter.Adapter(async_engine, db_class=CasbinRule)

        enforcer = casbin.Enforcer(RBAC_MODEL_CONF, adapter)

        return enforcer

    async def rbac_verify(self, request: Request, _: str = Depends(oauth2_schema)) -> None:
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
        # 免鉴权的接口
        method = request.method
        path = request.url.path
        if (method, path) in settings.CASBIN_EXCLUDE:
            return
        # 检测角色数据权限范围
        user_roles = request.user.roles
        data_scope = any(role.data_scope == 1 for role in user_roles)
        if data_scope:
            return
        if settings.MENU_PERMISSION:
            # 菜单权限校验
            path_auth = request.url.path.replace('/api/v1', '').replace('/', ':')
            menu_perms = []
            for role in user_roles:
                menu_perms.extend([menu.perms for menu in role.menus])
            if not menu_perms or path_auth not in menu_perms:
                raise AuthorizationError
        else:
            # casbin 权限校验
            user_uuid = request.user.user_uuid
            enforcer = self.enforcer()
            if not enforcer.enforce(user_uuid, path, method):
                raise AuthorizationError


RBAC = RBAC()
RbacEnforcer = RBAC.enforcer()
# RBAC 依赖注入
DependsRBAC = Depends(RBAC.rbac_verify)
