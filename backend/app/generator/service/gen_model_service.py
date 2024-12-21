#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from backend.app.generator.crud.crud_gen_model import gen_model_dao
from backend.app.generator.model import GenModel
from backend.app.generator.schema.gen_model import CreateGenModelParam, UpdateGenModelParam
from backend.common.enums import GenModelMySQLColumnType
from backend.common.exception import errors
from backend.database.db import async_db_session
from backend.utils.type_conversion import sql_type_to_pydantic


class GenModelService:
    @staticmethod
    async def get(*, pk: int) -> GenModel:
        async with async_db_session() as db:
            gen_model = await gen_model_dao.get(db, pk)
            return gen_model

    @staticmethod
    async def get_types() -> list[str]:
        types = GenModelMySQLColumnType.get_member_keys()
        types.sort()
        return types

    @staticmethod
    async def get_by_business(*, business_id: int) -> Sequence[GenModel]:
        async with async_db_session() as db:
            gen_models = await gen_model_dao.get_all_by_business_id(db, business_id)
            return gen_models

    @staticmethod
    async def create(*, obj: CreateGenModelParam) -> None:
        async with async_db_session.begin() as db:
            gen_models = await gen_model_dao.get_all_by_business_id(db, obj.gen_business_id)
            if obj.name in [gen_model.name for gen_model in gen_models]:
                raise errors.ForbiddenError(msg='禁止添加相同列到同一模型表')
            pd_type = sql_type_to_pydantic(obj.type)
            await gen_model_dao.create(db, obj, pd_type=pd_type)

    @staticmethod
    async def update(*, pk: int, obj: UpdateGenModelParam) -> int:
        async with async_db_session.begin() as db:
            model = await gen_model_dao.get(db, pk)
            if obj.name != model.name:
                gen_models = await gen_model_dao.get_all_by_business_id(db, obj.gen_business_id)
                if obj.name in [gen_model.name for gen_model in gen_models]:
                    raise errors.ForbiddenError(msg='模型列名已存在')
            pd_type = sql_type_to_pydantic(obj.type)
            count = await gen_model_dao.update(db, pk, obj, pd_type=pd_type)
            return count

    @staticmethod
    async def delete(*, pk: int) -> int:
        async with async_db_session.begin() as db:
            count = await gen_model_dao.delete(db, pk)
            return count


gen_model_service: GenModelService = GenModelService()
