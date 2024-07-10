#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from backend.app.generator.crud.crud_gen_model import gen_model_dao
from backend.app.generator.model import GenModel
from backend.app.generator.schema.gen_model import CreateGenModelParam, UpdateGenModelParam
from backend.common.exception import errors
from backend.database.db_mysql import async_db_session


class GenModelService:
    @staticmethod
    async def get_by_business(*, business_id: int) -> Sequence[GenModel]:
        async with async_db_session() as db:
            gen_model = await gen_model_dao.get_by_business_id(db, business_id)
            return gen_model

    @staticmethod
    async def create(*, obj: CreateGenModelParam) -> None:
        async with async_db_session.begin() as db:
            gen_models = await gen_model_dao.get_by_business_id(db, obj.gen_business_id)
            if gen_models:
                if obj.name in [name.name for name in gen_models]:
                    raise errors.ForbiddenError(msg='禁止添加相同列到模型表')
            await gen_model_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateGenModelParam) -> int:
        async with async_db_session.begin() as db:
            gen_models = await gen_model_dao.get_by_business_id(obj.gen_business_id)
            if gen_models:
                if obj.name in [name.name for name in gen_models]:
                    raise errors.ForbiddenError(msg='禁止添加相同列到模型表')
            count = await gen_model_dao.update(db, pk, obj)
            return count

    @staticmethod
    async def delete(*, pk: int) -> int:
        async with async_db_session.begin() as db:
            count = await gen_model_dao.delete(db, pk)
            return count


gen_model_service = GenModelService()
