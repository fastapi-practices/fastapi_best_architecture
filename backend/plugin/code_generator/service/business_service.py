#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from backend.common.exception import errors
from backend.database.db import async_db_session
from backend.plugin.code_generator.crud.crud_business import gen_business_dao
from backend.plugin.code_generator.model import GenBusiness
from backend.plugin.code_generator.schema.business import CreateGenBusinessParam, UpdateGenBusinessParam


class GenBusinessService:
    """Code Generation Business Services"""

    @staticmethod
    async def get(*, pk: int) -> GenBusiness:
        """
        GET SPECIFIED ID OPERATIONS

        :param pk: Operations ID
        :return:
        """
        async with async_db_session() as db:
            business = await gen_business_dao.get(db, pk)
            if not business:
                raise errors.NotFoundError(msg='Code Generation Business does not exist')
            return business

    @staticmethod
    async def get_all() -> Sequence[GenBusiness]:
        """Get all operations"""
        async with async_db_session() as db:
            return await gen_business_dao.get_all(db)

    @staticmethod
    async def create(*, obj: CreateGenBusinessParam) -> None:
        """
        Create Business

        :param obj: create business parameters
        :return:
        """
        async with async_db_session.begin() as db:
            business = await gen_business_dao.get_by_name(db, obj.table_name)
            if business:
                raise errors.ForbiddenError(msg='Code Generation Business Exists')
            await gen_business_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateGenBusinessParam) -> int:
        """
        Business update

        :param pk: Operations ID
        :param obj: update operational parameters
        :return:
        """
        async with async_db_session.begin() as db:
            return await gen_business_dao.update(db, pk, obj)

    @staticmethod
    async def delete(*, pk: int) -> int:
        """
        Delete Business

        :param pk: Operations ID
        :return:
        """
        async with async_db_session.begin() as db:
            return await gen_business_dao.delete(db, pk)


gen_business_service: GenBusinessService = GenBusinessService()
