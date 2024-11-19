#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any

from fastapi import Request
from sqlalchemy import ColumnElement, or_, select

from backend.app.admin.model import Dept
from backend.app.admin.model.m2m import sys_role_dept
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


def filter_data_scope(request: Request, model: Any) -> ColumnElement[bool]:
    """
    过滤用户数据范围（当前设计存在较大弊端，仅供参考）

    :param request: 接口请求对象
    :param model: 需要进行数据过滤的 sqlalchemy 模型
    :return:
    """
    user = request.user

    # 超级管理员可查看所有数据
    if user.is_superuser:
        return or_(1 == 1)

    user_id = user.id
    user_roles = user.roles

    # 无角色只能查看自己数据
    if not user_roles:
        return or_(getattr(model, 'created_by') == user_id if hasattr(model, 'created_by') else 1 == 0)

    data_scope = min(role.data_scope for role in user_roles if role.status == 1)
    user_dept_id = user.dept_id

    # 全部数据权限
    if data_scope == 0:
        return or_(1 == 1)

    # 自定义数据权限
    elif data_scope == 1:
        dept_ids = select(sys_role_dept.c.dept_id).where(
            sys_role_dept.c.role_id.in_(role.id for role in user_roles if role.status == 1)
        )
        return or_(getattr(model, 'dept_id').in_(dept_ids) if hasattr(model, 'dept_id') else 1 == 0)

    # 部门及以下数据权限
    elif data_scope == 2:
        child_dept_ids = select(Dept.id).where(or_(Dept.id == user_dept_id, Dept.parent_id == user_dept_id))
        return or_(getattr(model, 'dept_id').in_(child_dept_ids) if hasattr(model, 'dept_id') else 1 == 0)

    # 本部门数据权限
    elif data_scope == 3:
        return or_(getattr(model, 'dept_id') == user_dept_id if hasattr(model, 'dept_id') else 1 == 0)

    # 仅本人数据权限
    elif data_scope == 4:
        return or_(getattr(model, 'created_by') == user_id if hasattr(model, 'created_by') else 1 == 0)

    # 默认
    else:
        return or_(1 == 0)
