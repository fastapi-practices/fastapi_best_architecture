#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from backend.app.generator.crud.crud_gen_business import gen_business_dao
from backend.app.generator.model import GenBusiness
from backend.app.generator.schema.gen_business import CreateGenBusinessParam, UpdateGenBusinessParam
from backend.common.exception import errors
from backend.database.db import async_db_session


class GenBusinessService:
    """代码生成业务服务类"""

    @staticmethod
    async def get(*, pk: int) -> GenBusiness:
        """
        获取指定 ID 的业务

        :param pk: 业务 ID
        :return:
        """
        async with async_db_session() as db:
            business = await gen_business_dao.get(db, pk)
            if not business:
                raise errors.NotFoundError(msg='代码生成业务不存在')
            return business

    @staticmethod
    async def get_all() -> Sequence[GenBusiness]:
        """获取所有业务"""
        async with async_db_session() as db:
            return await gen_business_dao.get_all(db)

    @staticmethod
    async def create(*, obj: CreateGenBusinessParam) -> None:
        """
        创建业务

        :param obj: 创建业务参数
        :return:
        """
        async with async_db_session.begin() as db:
            business = await gen_business_dao.get_by_name(db, obj.table_name_en)
            if business:
                raise errors.ForbiddenError(msg='代码生成业务已存在')
            await gen_business_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateGenBusinessParam) -> int:
        """
        更新业务

        :param pk: 业务 ID
        :param obj: 更新业务参数
        :return:
        """
        async with async_db_session.begin() as db:
            return await gen_business_dao.update(db, pk, obj)

    @staticmethod
    async def delete(*, pk: int) -> int:
        """
        删除业务

        :param pk: 业务 ID
        :return:
        """
        async with async_db_session.begin() as db:
            return await gen_business_dao.delete(db, pk)


gen_business_service: GenBusinessService = GenBusinessService()
