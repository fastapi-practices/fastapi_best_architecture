#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any

from fastapi import Request
from sqlalchemy import Select

from backend.common.exception.errors import ServerError
from backend.core.conf import settings


class RequestPermission:
    """
    请求权限，仅用于角色菜单RBAC

    Tip:
        使用此请求权限时，需要将 `Depends(RequestPermission('xxx'))` 在 `DependsRBAC` 之前设置，
        因为 fastapi 当前版本的接口依赖注入按正序执行，意味着 RBAC 标识会在验证前被设置
    """

    def __init__(self, value: str):
        self.value = value

    async def __call__(self, request: Request):
        if settings.PERMISSION_MODE == 'role-menu':
            if not isinstance(self.value, str):
                raise ServerError
            # 附加权限标识
            request.state.permission = self.value


def filter_user_data_scope(request: Request, model: Any, stmt: Select) -> Select:
    """
    筛选用户数据范围

    使用场景：对于非后台管理数据，需要在前端界面向用户进行展示的数据

    :param request: 接口请求对象
    :param model: 当前需要进行数据过滤的 sqlalchemy 模型
    :param stmt: 需要进行数据筛选的 stmt（select） 语句
    :return:
    """
    user_roles = request.user.roles
    dept_roles = request.user.dept.roles
    user_roles.extend(dept_roles)
    data_scope = min(role.data_scope for role in set(user_roles))

    # 全部数据
    if data_scope == 0:
        stmt = stmt
    # 自定义数据（自选部门）
    elif data_scope == 1:
        ...
    # 所在部门及以下数据
    elif data_scope == 2:
        ...  # TODO
    # 所在部门数据
    elif data_scope == 3:
        ...
    # 仅本人数据
    elif data_scope == 4:
        stmt = stmt.where(model.create_user == request.user.id)

    return stmt
