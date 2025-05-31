#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import Request
from sqlalchemy import ColumnElement, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.admin.crud.crud_data_scope import data_scope_dao
from backend.common.enums import RoleDataRuleExpressionType, RoleDataRuleOperatorType
from backend.common.exception import errors
from backend.common.exception.errors import ServerError
from backend.core.conf import settings
from backend.utils.import_parse import dynamic_import_data_model


class RequestPermission:
    """
    请求权限验证器，用于角色菜单 RBAC 权限控制

    注意：
        使用此请求权限时，需要将 `Depends(RequestPermission('xxx'))` 在 `DependsRBAC` 之前设置，
        因为 FastAPI 当前版本的接口依赖注入按正序执行，意味着 RBAC 标识会在验证前被设置
    """

    def __init__(self, value: str) -> None:
        """
        初始化请求权限验证器

        :param value: 权限标识
        :return:
        """
        self.value = value

    async def __call__(self, request: Request) -> None:
        """
        验证请求权限

        :param request: FastAPI 请求对象
        :return:
        """
        if settings.RBAC_ROLE_MENU_MODE:
            if not isinstance(self.value, str):
                raise ServerError
            # 附加权限标识到请求状态
            request.state.permission = self.value


async def filter_data_permission(db: AsyncSession, request: Request) -> ColumnElement[bool]:
    """
    过滤数据权限，控制用户可见数据范围

    使用场景：
        - 控制用户能看到哪些数据

    :param db: 数据库会话
    :param request: FastAPI 请求对象
    :return:
    """
    # 是否过滤数据权限
    if request.user.is_superuser:
        return or_(1 == 1)

    for role in request.user.roles:
        if not role.is_filter_scopes:
            return or_(1 == 1)

    # 获取数据范围
    unique_data_scopes = {}
    for role in request.user.roles:
        for scope in role.scopes:
            if scope.status:
                unique_data_scopes[scope.id] = scope

    # 转换为列表
    data_scopes = list(unique_data_scopes.values())

    # 无规则用户不做过滤
    if not data_scopes:
        return or_(1 == 1)

    # 获取数据范围规则
    unique_data_rules = {}
    for data_scope in data_scopes:
        data_scope_with_relation = await data_scope_dao.get_with_relation(db, data_scope.id)
        for rule in data_scope_with_relation.rules:
            unique_data_rules[rule.id] = rule

    # 转换为列表
    data_rule_list = list(unique_data_rules.values())

    where_and_list = []
    where_or_list = []

    for data_rule in data_rule_list:
        # 验证规则模型
        rule_model = data_rule.model
        if rule_model not in settings.DATA_PERMISSION_MODELS:
            raise errors.NotFoundError(msg='数据规则模型不存在')
        model_ins = dynamic_import_data_model(settings.DATA_PERMISSION_MODELS[rule_model])

        # 验证规则列
        model_columns = [
            key for key in model_ins.__table__.columns.keys() if key not in settings.DATA_PERMISSION_COLUMN_EXCLUDE
        ]
        column = data_rule.column
        if column not in model_columns:
            raise errors.NotFoundError(msg='数据规则模型列不存在')

        # 构建过滤条件
        column_obj = getattr(model_ins, column)
        rule_expression = data_rule.expression
        condition = None
        match rule_expression:
            case RoleDataRuleExpressionType.eq:
                condition = column_obj == data_rule.value
            case RoleDataRuleExpressionType.ne:
                condition = column_obj != data_rule.value
            case RoleDataRuleExpressionType.gt:
                condition = column_obj > data_rule.value
            case RoleDataRuleExpressionType.ge:
                condition = column_obj >= data_rule.value
            case RoleDataRuleExpressionType.lt:
                condition = column_obj < data_rule.value
            case RoleDataRuleExpressionType.le:
                condition = column_obj <= data_rule.value
            case RoleDataRuleExpressionType.in_:
                values = data_rule.value.split(',') if isinstance(data_rule.value, str) else data_rule.value
                condition = column_obj.in_(values)
            case RoleDataRuleExpressionType.not_in:
                values = data_rule.value.split(',') if isinstance(data_rule.value, str) else data_rule.value
                condition = column_obj.not_in(values)

        # 根据运算符添加到对应列表
        if condition is not None:
            match data_rule.operator:
                case RoleDataRuleOperatorType.AND:
                    where_and_list.append(condition)
                case RoleDataRuleOperatorType.OR:
                    where_or_list.append(condition)

    # 组合所有条件
    where_list = []
    if where_and_list:
        where_list.append(and_(*where_and_list))
    if where_or_list:
        where_list.append(or_(*where_or_list))

    return or_(*where_list) if where_list else or_(1 == 1)
