#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import casbin
import casbin_sqlalchemy_adapter

from fastapi import Request, Depends

from backend.app.common.exception.errors import AuthorizationError
from backend.app.common.jwt import CurrentUser
from backend.app.core.conf import settings
from backend.app.core.path_conf import RBAC_MODEL_CONF
from backend.app.models.sys_casbin_rule import CasbinRule


class RBAC:
    def __init__(self):
        self._CASBIN_DATABASE_URL = f'mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_DATABASE}?charset={settings.DB_CHARSET}'

    def get_casbin_enforcer(self) -> casbin.Enforcer:
        """
        由于 casbin_sqlalchemy_adapter 内部使用的 SQLAlchemy 同步, 这里只能使用: mysql+pymysql

        :return:
        """
        adapter = casbin_sqlalchemy_adapter.Adapter(self._CASBIN_DATABASE_URL, db_class=CasbinRule)

        enforcer = casbin.Enforcer(RBAC_MODEL_CONF, adapter)

        return enforcer

    async def rbac_verify(self, request: Request, user: CurrentUser):
        """
        权限校验，超级用户跳过校验，默认拥有所有权限

        :param request:
        :param user:
        :return:
        """
        user_uuid = user.user_uuid
        user_roles = user.roles
        role_data_scope = [role.data_scope for role in user_roles]
        path = request.url.path
        method = request.method

        if user.is_superuser:
            ...

        for ce in settings.CASBIN_EXCLUDE:
            if ce['method'] == method and ce['path'] == path:
                ...

        if 1 in set(role_data_scope):
            ...

        enforcer = self.get_casbin_enforcer()
        if not enforcer.enforce(user_uuid, path, method):
            raise AuthorizationError


rbac = RBAC()
# RBAC 依赖注入
CurrentRBAC = Depends(rbac.rbac_verify)
