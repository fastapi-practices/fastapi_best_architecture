#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from fastapi import Request
from sqlalchemy import Select

from backend.app.admin.crud.crud_data_rule import data_rule_dao
from backend.app.admin.crud.crud_role import role_dao
from backend.app.admin.model import DataRule
from backend.app.admin.schema.data_rule import CreateDataRuleParam, UpdateDataRuleParam
from backend.common.exception import errors
from backend.core.conf import settings
from backend.database.db import async_db_session
from backend.database.redis import redis_client
from backend.utils.import_parse import dynamic_import_data_model


class DataRuleService:
    @staticmethod
    async def get(*, pk: int) -> DataRule:
        async with async_db_session() as db:
            data_rule = await data_rule_dao.get(db, pk)
            if not data_rule:
                raise errors.NotFoundError(msg='数据规则不存在')
            return data_rule

    @staticmethod
    async def get_role_rules(*, pk: int) -> list[int]:
        async with async_db_session() as db:
            role = await role_dao.get_with_relation(db, pk)
            if not role:
                raise errors.NotFoundError(msg='角色不存在')
            rule_ids = [rule.id for rule in role.rules]
            return rule_ids

    @staticmethod
    async def get_models() -> list[str]:
        return list(settings.DATA_PERMISSION_MODELS.keys())

    @staticmethod
    async def get_columns(model: str) -> list[str]:
        if model not in settings.DATA_PERMISSION_MODELS:
            raise errors.NotFoundError(msg='数据模型不存在')
        try:
            model_ins = dynamic_import_data_model(settings.DATA_PERMISSION_MODELS[model])
        except (ImportError, AttributeError):
            raise errors.ServerError(msg=f'数据模型 {model} 动态导入失败，请联系系统超级管理员')
        model_columns = [
            key for key in model_ins.__table__.columns.keys() if key not in settings.DATA_PERMISSION_COLUMN_EXCLUDE
        ]
        return model_columns

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
            await data_rule_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateDataRuleParam) -> int:
        async with async_db_session.begin() as db:
            data_rule = await data_rule_dao.get(db, pk)
            if not data_rule:
                raise errors.NotFoundError(msg='数据权限规则不存在')
            count = await data_rule_dao.update(db, pk, obj)
            return count

    @staticmethod
    async def delete(*, request: Request, pk: list[int]) -> int:
        async with async_db_session.begin() as db:
            count = await data_rule_dao.delete(db, pk)
            await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{request.user.id}')
            return count


data_rule_service: DataRuleService = DataRuleService()
