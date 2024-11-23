#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select

from backend.app.admin.crud.crud_data_rule import data_rule_dao
from backend.app.admin.crud.crud_data_rule_type import data_rule_type_dao
from backend.app.admin.model import DataRule
from backend.app.admin.schema.data_rule import CreateDataRuleParam, UpdateDataRuleParam
from backend.common.exception import errors
from backend.database.db_mysql import async_db_session


class DataRuleService:
    @staticmethod
    async def get(*, pk: int) -> DataRule:
        async with async_db_session() as db:
            data_rule = await data_rule_dao.get(db, pk)
            if not data_rule:
                raise errors.NotFoundError(msg='数据规则不存在')
            return data_rule

    @staticmethod
    async def get_models():
        return

    @staticmethod
    async def get_select(*, name: str = None) -> Select:
        return await data_rule_dao.get_list(name=name)

    @staticmethod
    async def get_all() -> Sequence[DataRule]:
        async with async_db_session() as db:
            data_rules = await data_rule_dao.get_all(db)
            return data_rules

    @staticmethod
    async def create(*, obj: CreateDataRuleParam) -> None:
        async with async_db_session.begin() as db:
            data_rule = await data_rule_dao.get_by_name(db, obj.name)
            if data_rule:
                raise errors.ForbiddenError(msg='数据权限规则已存在')
            data_rule_type = await data_rule_type_dao.get(db, obj.type_id)
            if not data_rule_type:
                raise errors.NotFoundError(msg='数据权限规则类型不存在')
            await data_rule_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateDataRuleParam) -> int:
        async with async_db_session.begin() as db:
            data_rule = await data_rule_dao.get(db, pk)
            if not data_rule:
                raise errors.NotFoundError(msg='数据权限规则不存在')
            data_rule_type = await data_rule_type_dao.get(db, obj.type_id)
            if not data_rule_type:
                raise errors.NotFoundError(msg='数据权限规则类型不存在')
            count = await data_rule_dao.update(db, pk, obj)
            return count

    @staticmethod
    async def delete(*, pk: list[int]) -> int:
        async with async_db_session.begin() as db:
            count = await data_rule_dao.delete(db, pk)
            return count


data_rule_service: DataRuleService = DataRuleService()
