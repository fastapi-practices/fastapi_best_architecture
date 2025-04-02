#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select

from backend.common.exception import errors
from backend.database.db import async_db_session
from backend.plugin.dict.crud.crud_dict_data import dict_data_dao
from backend.plugin.dict.crud.crud_dict_type import dict_type_dao
from backend.plugin.dict.model import DictData
from backend.plugin.dict.schema.dict_data import CreateDictDataParam, UpdateDictDataParam


class DictDataService:
    """字典数据服务类"""

    @staticmethod
    async def get(*, pk: int) -> DictData:
        """
        获取字典数据详情

        :param pk: 字典数据 ID
        :return:
        """
        async with async_db_session() as db:
            dict_data = await dict_data_dao.get_with_relation(db, pk)
            if not dict_data:
                raise errors.NotFoundError(msg='字典数据不存在')
            return dict_data

    @staticmethod
    async def get_select(*, label: str | None = None, value: str | None = None, status: int | None = None) -> Select:
        """
        获取字典数据列表查询条件

        :param label: 字典数据标签
        :param value: 字典数据键值
        :param status: 状态
        :return:
        """
        return await dict_data_dao.get_list(label=label, value=value, status=status)

    @staticmethod
    async def create(*, obj: CreateDictDataParam) -> None:
        """
        创建字典数据

        :param obj: 字典数据创建参数
        :return:
        """
        async with async_db_session.begin() as db:
            dict_data = await dict_data_dao.get_by_label(db, obj.label)
            if dict_data:
                raise errors.ForbiddenError(msg='字典数据已存在')
            dict_type = await dict_type_dao.get(db, obj.type_id)
            if not dict_type:
                raise errors.NotFoundError(msg='字典类型不存在')
            await dict_data_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateDictDataParam) -> int:
        """
        更新字典数据

        :param pk: 字典数据 ID
        :param obj: 字典数据更新参数
        :return:
        """
        async with async_db_session.begin() as db:
            dict_data = await dict_data_dao.get(db, pk)
            if not dict_data:
                raise errors.NotFoundError(msg='字典数据不存在')
            if dict_data.label != obj.label:
                if await dict_data_dao.get_by_label(db, obj.label):
                    raise errors.ForbiddenError(msg='字典数据已存在')
            dict_type = await dict_type_dao.get(db, obj.type_id)
            if not dict_type:
                raise errors.NotFoundError(msg='字典类型不存在')
            count = await dict_data_dao.update(db, pk, obj)
            return count

    @staticmethod
    async def delete(*, pk: list[int]) -> int:
        """
        删除字典数据

        :param pk: 字典数据 ID 列表
        :return:
        """
        async with async_db_session.begin() as db:
            count = await dict_data_dao.delete(db, pk)
            return count


dict_data_service: DictDataService = DictDataService()
