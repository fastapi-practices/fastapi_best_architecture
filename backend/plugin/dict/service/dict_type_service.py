#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select

from backend.common.exception import errors
from backend.database.db import async_db_session
from backend.plugin.dict.crud.crud_dict_type import dict_type_dao
from backend.plugin.dict.schema.dict_type import CreateDictTypeParam, UpdateDictTypeParam


class DictTypeService:
    """Dictionary type service class"""

    @staticmethod
    async def get_select(*, name: str | None, code: str | None, status: int | None) -> Select:
        """
        Get dictionary type list query conditions

        :param name: dictionary type name
        :param code: dictionary type encoding
        :param status: status
        :return:
        """
        return await dict_type_dao.get_list(name=name, code=code, status=status)

    @staticmethod
    async def create(*, obj: CreateDictTypeParam) -> None:
        """
        Create dictionary type

        :param obj: dictionary type creation parameters
        :return:
        """
        async with async_db_session.begin() as db:
            dict_type = await dict_type_dao.get_by_code(db, obj.code)
            if dict_type:
                raise errors.ForbiddenError(msg='Dictionary type already exists')
            await dict_type_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateDictTypeParam) -> int:
        """
        Update dictionary type

        :param pk: dictionary type ID
        :param obj: dictionary type update parameters
        :return:
        """
        async with async_db_session.begin() as db:
            dict_type = await dict_type_dao.get(db, pk)
            if not dict_type:
                raise errors.NotFoundError(msg='Dictionary type does not exist')
            if dict_type.code != obj.code:
                if await dict_type_dao.get_by_code(db, obj.code):
                    raise errors.ForbiddenError(msg='Dictionary type already exists')
            count = await dict_type_dao.update(db, pk, obj)
            return count

    @staticmethod
    async def delete(*, pk: list[int]) -> int:
        """
        Remove Dictionary Type

        :param pk: dictionary type ID list
        :return:
        """
        async with async_db_session.begin() as db:
            count = await dict_type_dao.delete(db, pk)
            return count


dict_type_service: DictTypeService = DictTypeService()
