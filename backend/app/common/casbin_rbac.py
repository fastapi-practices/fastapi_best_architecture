#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import casbin
import casbin_async_sqlalchemy_adapter
from fastapi import Request, Depends

from backend.app.common.exception.errors import AuthorizationError
from backend.app.common.jwt import DependsJwtAuth
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

    async def rbac_verify(self, request: Request, _: str = DependsJwtAuth) -> None:
        """
        权限校验

        :param request:
        :param _:
        :return:
        """
        super_user = request.user.is_superuser
        if super_user:
            return

        method = request.method
        path = request.url.path
        if (method, path) in settings.CASBIN_EXCLUDE:
            return

        user_roles = request.user.roles
        data_scope = [role.data_scope for role in user_roles if role.data_scope == 1]
        if data_scope:
            return

        # TODO: 通过 redis 做鉴权查询优化，减少数据库查询
        user_uuid = request.user.user_uuid
        enforcer = self.enforcer()
        if not enforcer.enforce(user_uuid, path, method):
            raise AuthorizationError


RBAC = RBAC()
RbacEnforcer = RBAC.enforcer()
# RBAC 依赖注入
DependsRBAC = Depends(RBAC.rbac_verify)
