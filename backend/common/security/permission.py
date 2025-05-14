#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import TYPE_CHECKING

from fastapi import Request
from sqlalchemy import ColumnElement, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.admin.crud.crud_data_scope import data_scope_dao
from backend.common.enums import RoleDataRuleExpressionType, RoleDataRuleOperatorType
from backend.common.exception import errors
from backend.common.exception.errors import ServerError
from backend.core.conf import settings
from backend.utils.import_parse import dynamic_import_data_model

if TYPE_CHECKING:
    from backend.app.admin.model import DataRule


class RequestPermission:
    """
    REQUEST PERMISSION CERTIFIER FOR ROLE MENU RBAC PERMISSION CONTROL

    Attention：
        Use this request permission to set `Depends' (RequestPermission('xx')) 'before `DependsRBAC '，
        Because the current version of the FastAPI interface relies on injection in order, which means that the RBAC identifier will be set before authentication
    """

    def __init__(self, value: str) -> None:
        """
        Initialization Request Permission Validator

        :param value: permission mark
        :return:
        """
        self.value = value

    async def __call__(self, request: Request) -> None:
        """
        Permission to verify a request

        :param request: FastAPI
        :return:
        """
        if settings.RBAC_ROLE_MENU_MODE:
            if not isinstance(self.value, str):
                raise ServerError
            # Additional Permissions Mark to Request Status
            request.state.permission = self.value


async def filter_data_permission(db: AsyncSession, request: Request) -> ColumnElement[bool]:
    """
    Filter Data Permissions to Control User Visible Data Ranges

    Use scene：
        - Control what data the user can see

    :param db: database session
    :param request: FastAPI
    :return:
    """
    # Access to user roles and data ranges
    data_scopes = []
    for role in request.user.roles:
        for scope in role.scopes:
            if scope.status:
                data_scopes.append(scope)

    # Super Administrators and Ungrateful Users do not filter
    if request.user.is_superuser or not data_scopes:
        print('super admin or no data scope')
        return or_(1 == 1)

    # Rules on access to data coverage
    data_rule_list: list[DataRule] = []
    for data_scope in data_scopes:
        data_scope_with_relation = await data_scope_dao.get_with_relation(db, data_scope.id)
        data_rule_list.extend(data_scope_with_relation.rules)

    # Heavy
    seen_data_rule_ids = set()
    new_data_rule_list = []
    for rule in data_rule_list:
        if rule.id not in seen_data_rule_ids:
            seen_data_rule_ids.add(rule.id)
            new_data_rule_list.append(rule)

    where_and_list = []
    where_or_list = []

    for data_rule in new_data_rule_list:
        # Model of certification rules
        rule_model = data_rule.model
        if rule_model not in settings.DATA_PERMISSION_MODELS:
            raise errors.NotFoundError(msg='Data rule model does not exist')
        model_ins = dynamic_import_data_model(
            settings.DATA_PERMISSION_MODELS[rule_model])

        # Authentication Rules Bar
        model_columns = [
            key for key in model_ins.__table__.columns.keys() if key not in settings.DATA_PERMISSION_COLUMN_EXCLUDE
        ]
        column = data_rule.column
        if column not in model_columns:
            raise errors.NotFoundError(
                msg='Data rule model column does not exist')

        # Build Filter Conditions
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
                values = data_rule.value.split(',') if isinstance(
                    data_rule.value, str) else data_rule.value
                condition = column_obj.in_(values)
            case RoleDataRuleExpressionType.not_in:
                values = data_rule.value.split(',') if isinstance(
                    data_rule.value, str) else data_rule.value
                condition = column_obj.not_in(values)

        # Add to the corresponding list by operator
        if condition is not None:
            match data_rule.operator:
                case RoleDataRuleOperatorType.AND:
                    where_and_list.append(condition)
                case RoleDataRuleOperatorType.OR:
                    where_or_list.append(condition)

    # Group All Conditions
    where_list = []
    if where_and_list:
        where_list.append(and_(*where_and_list))
    if where_or_list:
        where_list.append(or_(*where_or_list))

    return or_(*where_list) if where_list else or_(1 == 1)
