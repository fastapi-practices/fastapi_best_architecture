#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import TYPE_CHECKING

from fastapi import Request
from sqlalchemy import ColumnElement, and_, or_

from backend.common.enums import RoleDataRuleExpressionType, RoleDataRuleOperatorType
from backend.common.exception import errors
from backend.common.exception.errors import ServerError
from backend.core.conf import settings
from backend.utils.import_parse import dynamic_import

if TYPE_CHECKING:
    from backend.app.admin.schema.data_rule import GetDataRuleListDetails


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


def filter_data_permission(request: Request) -> ColumnElement[bool]:
    """
    过滤数据权限

    使用场景：用户登录前台后，控制其能看到哪些数据

    :param request:
    :return:
    """
    user_data_rules: list[GetDataRuleListDetails] = request.user.roles.rules

    # 超级管理员和无规则用户不做过滤
    if request.user.is_superuser or not user_data_rules:
        return or_(1 == 1)

    where_and_list = []
    where_or_list = []
    allowed_models = frozenset(m.split('.')[-1] for m in settings.ALLOWED_MODELS)

    for rule in user_data_rules:
        rule_model = rule.model
        if rule_model not in allowed_models:
            raise errors.NotFoundError(msg='数据模型不存在')
        try:
            model_ins = dynamic_import(rule_model)
        except Exception:
            raise errors.ServerError(msg='数据模型动态调用失败，请联系系统超级管理员')
        model_columns = model_ins.__table__.columns.keys()
        column = rule.column
        if column not in model_columns:
            raise errors.NotFoundError(msg='数据模型列不存在')

        # 获取模型的列对象
        column_obj = getattr(model_ins, column)
        rule_expression = rule.expression

        # 根据表达式类型构建条件
        condition = None
        if rule_expression == RoleDataRuleExpressionType.eq:
            condition = column_obj == rule.value
        elif rule_expression == RoleDataRuleExpressionType.ne:
            condition = column_obj != rule.value
        elif rule_expression == RoleDataRuleExpressionType.gt:
            condition = column_obj > rule.value
        elif rule_expression == RoleDataRuleExpressionType.ge:
            condition = column_obj >= rule.value
        elif rule_expression == RoleDataRuleExpressionType.lt:
            condition = column_obj < rule.value
        elif rule_expression == RoleDataRuleExpressionType.le:
            condition = column_obj <= rule.value
        elif rule_expression == RoleDataRuleExpressionType.in_:
            values = rule.value.split(',') if isinstance(rule.value, str) else rule.value
            condition = column_obj.in_(values)
        elif rule.expression == RoleDataRuleExpressionType.not_in:
            values = rule.value.split(',') if isinstance(rule.value, str) else rule.value
            condition = ~column_obj.in_(values)

        if condition is not None:
            rule_operator = rule.operator
            if rule_operator == RoleDataRuleOperatorType.AND:
                where_and_list.append(condition)
            elif rule_operator == RoleDataRuleOperatorType.OR:
                where_or_list.append(condition)

    # 组合条件
    where_list = []
    if where_and_list:
        where_list.append(and_(*where_and_list))
    if where_or_list:
        where_list.append(or_(*where_or_list))

    return or_(*where_list) if where_list else or_(1 == 1)
