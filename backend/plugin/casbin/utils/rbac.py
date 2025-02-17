#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import casbin
import casbin_async_sqlalchemy_adapter

from fastapi import Request

from backend.common.exception.errors import AuthorizationError
from backend.database.db import async_engine
from backend.plugin.casbin.conf import casbin_settings
from backend.plugin.casbin.model import CasbinRule


async def casbin_enforcer() -> casbin.AsyncEnforcer:
    """
    获取 casbin 执行器

    :return:
    """
    # 模型定义：https://casbin.org/zh/docs/category/model
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


async def casbin_verify(request: Request) -> None:
    """
    Casbin 权限校验

    :param request:
    :return:
    """
    method = request.method
    path = request.url.path

    # casbin 鉴权白名单
    if (method, path) in casbin_settings.RBAC_CASBIN_EXCLUDE:
        return

    # casbin 权限校验
    user_uuid = request.user.uuid
    enforcer = await casbin_enforcer()
    if not enforcer.enforce(user_uuid, path, method):
        raise AuthorizationError
