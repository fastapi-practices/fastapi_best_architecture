#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from backend.app.generator.crud.crud_gen_model import gen_model_dao
from backend.app.generator.model import GenModel
from backend.database.db_mysql import async_db_session


class GenModelService:
    @staticmethod
    async def get_with_relation(*, business_id: int) -> Sequence[GenModel]:
        async with async_db_session() as db:
            gen_model = await gen_model_dao.get_with_relation(db, business_id)
            return gen_model

    @staticmethod
    async def create() -> None: ...

    @staticmethod
    async def update() -> int: ...

    @staticmethod
    async def delete() -> int: ...


gen_model_service = GenModelService()
