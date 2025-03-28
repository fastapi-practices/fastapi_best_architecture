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
    """代码生成模型服务类"""

    @staticmethod
    async def get(*, pk: int) -> GenModel:
        """
        获取指定 ID 的模型

        :param pk: 模型 ID
        :return:
        """
        async with async_db_session() as db:
            model = await gen_model_dao.get(db, pk)
            if not model:
                raise errors.NotFoundError(msg='代码生成模型不存在')
            return model

    @staticmethod
    async def get_types() -> list[str]:
        """获取所有 MySQL 列类型"""
        types = GenModelMySQLColumnType.get_member_keys()
        types.sort()
        return types

    @staticmethod
    async def get_by_business(*, business_id: int) -> Sequence[GenModel]:
        """
        获取指定业务的所有模型

        :param business_id: 业务 ID
        :return:
        """
        async with async_db_session() as db:
            return await gen_model_dao.get_all_by_business(db, business_id)

    @staticmethod
    async def create(*, obj: CreateGenModelParam) -> None:
        """
        创建模型

        :param obj: 创建模型参数
        :return:
        """
        async with async_db_session.begin() as db:
            gen_models = await gen_model_dao.get_all_by_business(db, obj.gen_business_id)
            if obj.name in [gen_model.name for gen_model in gen_models]:
                raise errors.ForbiddenError(msg='禁止添加相同列到同一模型表')

            pd_type = sql_type_to_pydantic(obj.type)
            await gen_model_dao.create(db, obj, pd_type=pd_type)

    @staticmethod
    async def update(*, pk: int, obj: UpdateGenModelParam) -> int:
        """
        更新模型

        :param pk: 模型 ID
        :param obj: 更新模型参数
        :return:
        """
        async with async_db_session.begin() as db:
            model = await gen_model_dao.get(db, pk)
            if obj.name != model.name:
                gen_models = await gen_model_dao.get_all_by_business(db, obj.gen_business_id)
                if obj.name in [gen_model.name for gen_model in gen_models]:
                    raise errors.ForbiddenError(msg='模型列名已存在')

            pd_type = sql_type_to_pydantic(obj.type)
            return await gen_model_dao.update(db, pk, obj, pd_type=pd_type)

    @staticmethod
    async def delete(*, pk: int) -> int:
        """
        删除模型

        :param pk: 模型 ID
        :return:
        """
        async with async_db_session.begin() as db:
            return await gen_model_dao.delete(db, pk)


gen_model_service: GenModelService = GenModelService()
