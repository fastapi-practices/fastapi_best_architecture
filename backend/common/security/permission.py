from functools import partial
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy import ColumnElement, and_, or_

from backend.common.context import ctx
from backend.common.enums import RoleDataRuleExpressionType, RoleDataRuleOperatorType
from backend.common.exception import errors
from backend.core.conf import settings
from backend.utils.import_parse import get_all_models


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
                raise errors.ServerError
            # 附加权限标识到请求状态
            ctx.permission = self.value


def get_data_permission_models() -> dict[str, object]:
    """获取所有可用于数据权限的模型"""
    return {model.__name__: model for model in get_all_models()}


def filter_data_permission(request: Request, model: object) -> ColumnElement[bool]:  # noqa: C901
    """
    过滤数据权限，控制用户可见数据范围

    使用场景：
        - 控制用户能看到哪些数据

    :param request: FastAPI 请求对象
    :param model: 需要应用数据权限的模型类
    :return:
    """
    # 超级管理员不过滤
    if request.user.is_superuser:
        return or_(1 == 1)

    # 角色未启用数据权限过滤
    for role in request.user.roles:
        if not role.is_filter_scopes:
            return or_(1 == 1)

    # 获取数据规则
    data_rules = set()
    for role in request.user.roles:
        for scope in role.scopes:
            if scope.status:
                data_rules.update(scope.rules)

    if not data_rules:
        return or_(1 == 1)

    where_and_list = []
    where_or_list = []
    current_model_name = model.__name__

    for data_rule in data_rules:
        # 只处理匹配当前模型的规则
        if data_rule.model != current_model_name:
            continue

        rule_column = data_rule.column
        if rule_column not in model.__table__.columns.keys():
            continue
        if rule_column in settings.DATA_PERMISSION_COLUMN_EXCLUDE:
            continue

        # 构建过滤条件
        column_obj = getattr(model, rule_column)
        condition = None
        match data_rule.expression:
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


def DataPermissionFilter(model: object) -> type[ColumnElement[bool]]:  # noqa: N802
    """
    指定模型的数据权限过滤器

    :param model: 模型类
    :return:
    """
    return Annotated[ColumnElement[bool], Depends(partial(filter_data_permission, model=model))]
