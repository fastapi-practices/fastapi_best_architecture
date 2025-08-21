#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from backend.common.exception import errors
from backend.database.db import async_db_session
from backend.plugin.code_generator.crud.crud_column import gen_column_dao
from backend.plugin.code_generator.enums import GenMySQLColumnType
from backend.plugin.code_generator.model import GenColumn
from backend.plugin.code_generator.schema.column import CreateGenColumnParam, UpdateGenColumnParam
from backend.plugin.code_generator.utils.type_conversion import sql_type_to_pydantic


class GenColumnService:
    """代码生成模型列服务类"""

    @staticmethod
    async def get(*, pk: int) -> GenColumn:
        """
        获取指定 ID 的模型列

        :param pk: 模型列 ID
        :return:
        """
        async with async_db_session() as db:
            column = await gen_column_dao.get(db, pk)
            if not column:
                raise errors.NotFoundError(msg='代码生成模型列不存在')
            return column

    @staticmethod
    async def get_types() -> list[str]:
        """获取所有 MySQL 列类型"""
        types = GenMySQLColumnType.get_member_keys()
        types.sort()
        return types

    @staticmethod
    async def get_columns(*, business_id: int) -> Sequence[GenColumn]:
        """
        获取指定业务的所有模型列

        :param business_id: 业务 ID
        :return:
        """
        async with async_db_session() as db:
            return await gen_column_dao.get_all_by_business(db, business_id)

    @staticmethod
    async def create(*, obj: CreateGenColumnParam) -> None:
        """
        创建模型列

        :param obj: 创建模型列参数
        :return:
        """
        async with async_db_session.begin() as db:
            gen_columns = await gen_column_dao.get_all_by_business(db, obj.gen_business_id)
            if obj.name in [gen_column.name for gen_column in gen_columns]:
                raise errors.ForbiddenError(msg='模型列已存在')

            pd_type = sql_type_to_pydantic(obj.type)
            await gen_column_dao.create(db, obj, pd_type=pd_type)

    @staticmethod
    async def update(*, pk: int, obj: UpdateGenColumnParam) -> int:
        """
        更新模型列

        :param pk: 模型列 ID
        :param obj: 更新模型列参数
        :return:
        """
        async with async_db_session.begin() as db:
            column = await gen_column_dao.get(db, pk)
            if obj.name != column.name:
                gen_columns = await gen_column_dao.get_all_by_business(db, obj.gen_business_id)
                if obj.name in [gen_column.name for gen_column in gen_columns]:
                    raise errors.ConflictError(msg='模型列名已存在')

            pd_type = sql_type_to_pydantic(obj.type)
            return await gen_column_dao.update(db, pk, obj, pd_type=pd_type)

    @staticmethod
    async def delete(*, pk: int) -> int:
        """
        删除模型列

        :param pk: 模型列 ID
        :return:
        """
        async with async_db_session.begin() as db:
            return await gen_column_dao.delete(db, pk)


gen_column_service: GenColumnService = GenColumnService()
