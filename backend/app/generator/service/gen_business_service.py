#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from backend.app.generator.crud.crud_gen_business import gen_business_dao
from backend.app.generator.model import GenBusiness
from backend.app.generator.schema.gen_business import CreateGenBusinessParam, UpdateGenBusinessParam
from backend.common.exception import errors
from backend.database.db import async_db_session


class GenBusinessService:
    @staticmethod
    async def get(*, pk: int) -> GenBusiness:
        async with async_db_session() as db:
            business = await gen_business_dao.get(db, pk)
            if not business:
                raise errors.NotFoundError(msg='代码生成业务不存在')
            return business

    @staticmethod
    async def get_all() -> Sequence[GenBusiness]:
        async with async_db_session() as db:
            businesses = await gen_business_dao.get_all(db)
            return businesses

    @staticmethod
    async def create(*, obj: CreateGenBusinessParam) -> None:
        async with async_db_session.begin() as db:
            business = await gen_business_dao.get_by_name(db, obj.table_name_en)
            if business:
                raise errors.ForbiddenError(msg='代码生成业务已存在')
            await gen_business_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateGenBusinessParam) -> int:
        async with async_db_session.begin() as db:
            count = await gen_business_dao.update(db, pk, obj)
            return count

    @staticmethod
    async def delete(*, pk: int) -> int:
        async with async_db_session.begin() as db:
            count = await gen_business_dao.delete(db, pk)
            return count


gen_business_service: GenBusinessService = GenBusinessService()
