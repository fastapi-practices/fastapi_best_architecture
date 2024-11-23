#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select

from backend.app.admin.crud.crud_data_rule_type import data_rule_type_dao
from backend.app.admin.model import DataRuleType
from backend.app.admin.schema.data_rule_type import CreateDataRuleTypeParam, UpdateDataRuleTypeParam
from backend.common.exception import errors
from backend.database.db_mysql import async_db_session


class DataRuleTypeService:
    @staticmethod
    async def get(*, pk: int) -> DataRuleType:
        async with async_db_session() as db:
            data_rule_type = await data_rule_type_dao.get(db, pk)
            if not data_rule_type:
                raise errors.NotFoundError(msg='数据规则类型不存在')
            return data_rule_type

    @staticmethod
    async def get_select() -> Select:
        return await data_rule_type_dao.get_list()

    @staticmethod
    async def get_all() -> Sequence[DataRuleType]:
        async with async_db_session() as db:
            data_rule_types = await data_rule_type_dao.get_all(db)
            return data_rule_types

    @staticmethod
    async def create(*, obj: CreateDataRuleTypeParam) -> None:
        async with async_db_session.begin() as db:
            data_rule_type = await data_rule_type_dao.get_by_name(db, obj.name)
            if data_rule_type:
                raise errors.ForbiddenError(msg='数据权限规则类型已存在')
            await data_rule_type_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateDataRuleTypeParam) -> int:
        async with async_db_session.begin() as db:
            data_rule_type = await data_rule_type_dao.get(db, pk)
            if not data_rule_type:
                raise errors.NotFoundError(msg='数据权限规则类型不存在')
            if data_rule_type.name != obj.name:
                if await data_rule_type_dao.get_by_name(db, obj.name):
                    raise errors.ForbiddenError(msg='数据权限规则类型已存在')
            count = await data_rule_type_dao.update(db, pk, obj)
            return count

    @staticmethod
    async def delete(*, pk: list[int]) -> int:
        async with async_db_session.begin() as db:
            count = await data_rule_type_dao.delete(db, pk)
            return count


data_rule_type_service: DataRuleTypeService = DataRuleTypeService()
