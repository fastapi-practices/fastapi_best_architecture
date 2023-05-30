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
    async def get_casbin_enforcer() -> casbin.Enforcer:
        """
        获取 casbin 执行器

        :return:
        """
        adapter = casbin_async_sqlalchemy_adapter.Adapter(async_engine, db_class=CasbinRule)

        enforcer = casbin.Enforcer(RBAC_MODEL_CONF, adapter)

        return enforcer

    async def rbac_verify(self, request: Request, _: str = DependsJwtAuth) -> None:
        """
        权限校验，超级用户跳过校验，默认拥有所有权限

        :param request:
        :param _:
        :return:
        """
        user_uuid = request.user.user_uuid
        user_roles = request.user.roles
        role_data_scope = [role.data_scope for role in user_roles]
        super_user = request.user.is_superuser
        path = request.url.path
        method = request.method

        if super_user:
            return

        for ce in settings.CASBIN_EXCLUDE:
            if ce['method'] == method and ce['path'] == path:
                return

        if 1 in set(role_data_scope):
            return

        # TODO: 通过 redis 做鉴权查询优化，减少数据库查询
        enforcer = await self.get_casbin_enforcer()
        if not enforcer.enforce(user_uuid, path, method):
            raise AuthorizationError


rbac = RBAC()
# RBAC 依赖注入
DependsRBAC = Depends(rbac.rbac_verify)
