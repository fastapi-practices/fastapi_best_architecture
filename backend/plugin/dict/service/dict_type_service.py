#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select

from backend.common.exception import errors
from backend.database.db import async_db_session
from backend.plugin.dict.crud.crud_dict_type import dict_type_dao
from backend.plugin.dict.model import DictType
from backend.plugin.dict.schema.dict_type import CreateDictTypeParam, DeleteDictTypeParam, UpdateDictTypeParam


class DictTypeService:
    """字典类型服务类"""

    @staticmethod
    async def get(*, pk) -> DictType:
        """
        获取字典类型详情

        :param pk: 字典类型 ID
        :return:
        """
        async with async_db_session() as db:
            dict_type = await dict_type_dao.get(db, pk)
            if not dict_type:
                raise errors.NotFoundError(msg='字典类型不存在')
            return dict_type

    @staticmethod
    async def get_all() -> Sequence[DictType]:
        async with async_db_session() as db:
            dict_datas = await dict_type_dao.get_all(db)
            return dict_datas

    @staticmethod
    async def get_select(*, name: str | None, code: str | None) -> Select:
        """
        获取字典类型列表查询条件

        :param name: 字典类型名称
        :param code: 字典类型编码
        :return:
        """
        return await dict_type_dao.get_list(name=name, code=code)

    @staticmethod
    async def create(*, obj: CreateDictTypeParam) -> None:
        """
        创建字典类型

        :param obj: 字典类型创建参数
        :return:
        """
        async with async_db_session.begin() as db:
            dict_type = await dict_type_dao.get_by_code(db, obj.code)
            if dict_type:
                raise errors.ConflictError(msg='字典类型已存在')
            await dict_type_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateDictTypeParam) -> int:
        """
        更新字典类型

        :param pk: 字典类型 ID
        :param obj: 字典类型更新参数
        :return:
        """
        async with async_db_session.begin() as db:
            dict_type = await dict_type_dao.get(db, pk)
            if not dict_type:
                raise errors.NotFoundError(msg='字典类型不存在')
            if dict_type.code != obj.code:
                if await dict_type_dao.get_by_code(db, obj.code):
                    raise errors.ConflictError(msg='字典类型已存在')
            count = await dict_type_dao.update(db, pk, obj)
            return count

    @staticmethod
    async def delete(*, obj: DeleteDictTypeParam) -> int:
        """
        批量删除字典类型

        :param obj: 字典类型 ID 列表
        :return:
        """
        async with async_db_session.begin() as db:
            count = await dict_type_dao.delete(db, obj.pks)
            return count


dict_type_service: DictTypeService = DictTypeService()
