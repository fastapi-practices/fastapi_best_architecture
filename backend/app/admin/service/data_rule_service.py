#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select

from backend.app.admin.crud.crud_data_rule import data_rule_dao
from backend.app.admin.model import DataRule
from backend.app.admin.schema.data_rule import CreateDataRuleParam, GetDataRuleColumnDetail, UpdateDataRuleParam
from backend.common.exception import errors
from backend.core.conf import settings
from backend.database.db import async_db_session
from backend.utils.import_parse import dynamic_import_data_model


class DataRuleService:
    """数据规则服务类"""

    @staticmethod
    async def get(*, pk: int) -> DataRule:
        """
        获取数据规则详情

        :param pk: 规则 ID
        :return:
        """
        async with async_db_session() as db:
            data_rule = await data_rule_dao.get(db, pk)
            if not data_rule:
                raise errors.NotFoundError(msg='数据规则不存在')
            return data_rule

    @staticmethod
    async def get_models() -> list[str]:
        """获取所有数据规则可用模型"""
        return list(settings.DATA_PERMISSION_MODELS.keys())

    @staticmethod
    async def get_columns(model: str) -> list[GetDataRuleColumnDetail]:
        """
        获取数据规则可用模型的字段列表

        :param model: 模型名称
        :return:
        """
        if model not in settings.DATA_PERMISSION_MODELS:
            raise errors.NotFoundError(msg='数据规则可用模型不存在')
        model_ins = dynamic_import_data_model(settings.DATA_PERMISSION_MODELS[model])

        model_columns = [
            GetDataRuleColumnDetail(key=column.key, comment=column.comment)
            for column in model_ins.__table__.columns
            if column.key not in settings.DATA_PERMISSION_COLUMN_EXCLUDE
        ]
        return model_columns

    @staticmethod
    async def get_select(*, name: str | None) -> Select:
        """
        获取数据规则列表查询条件

        :param name: 规则名称
        :return:
        """
        return await data_rule_dao.get_list(name=name)

    @staticmethod
    async def get_all() -> Sequence[DataRule]:
        """获取所有数据规则"""
        async with async_db_session() as db:
            data_rules = await data_rule_dao.get_all(db)
            return data_rules

    @staticmethod
    async def create(*, obj: CreateDataRuleParam) -> None:
        """
        创建数据规则

        :param obj: 规则创建参数
        :return:
        """
        async with async_db_session.begin() as db:
            data_rule = await data_rule_dao.get_by_name(db, obj.name)
            if data_rule:
                raise errors.ForbiddenError(msg='数据规则已存在')
            await data_rule_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateDataRuleParam) -> int:
        """
        更新数据规则

        :param pk: 规则 ID
        :param obj: 规则更新参数
        :return:
        """
        async with async_db_session.begin() as db:
            data_rule = await data_rule_dao.get(db, pk)
            if not data_rule:
                raise errors.NotFoundError(msg='数据规则不存在')
            if data_rule.name != obj.name:
                if await data_rule_dao.get_by_name(db, obj.name):
                    raise errors.ForbiddenError(msg='数据规则已存在')
            count = await data_rule_dao.update(db, pk, obj)
            return count

    @staticmethod
    async def delete(*, pk: list[int]) -> int:
        """
        删除数据规则

        :param pk: 规则 ID 列表
        :return:
        """
        async with async_db_session.begin() as db:
            count = await data_rule_dao.delete(db, pk)
            return count


data_rule_service: DataRuleService = DataRuleService()
