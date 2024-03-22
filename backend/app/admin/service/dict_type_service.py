#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select

from backend.app.admin.crud.crud_dict_type import dict_type_dao
from backend.app.admin.schema.dict_type import CreateDictTypeParam, UpdateDictTypeParam
from backend.common.exception import errors
from backend.database.db_mysql import async_db_session


class DictTypeService:
    @staticmethod
    async def get_select(*, name: str = None, code: str = None, status: int = None) -> Select:
        return await dict_type_dao.get_list(name=name, code=code, status=status)

    @staticmethod
    async def create(*, obj: CreateDictTypeParam) -> None:
        async with async_db_session.begin() as db:
            dict_type = await dict_type_dao.get_by_code(db, obj.code)
            if dict_type:
                raise errors.ForbiddenError(msg='字典类型已存在')
            await dict_type_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateDictTypeParam) -> int:
        async with async_db_session.begin() as db:
            dict_type = await dict_type_dao.get(db, pk)
            if not dict_type:
                raise errors.NotFoundError(msg='字典类型不存在')
            if dict_type.code != obj.code:
                if await dict_type_dao.get_by_code(db, obj.code):
                    raise errors.ForbiddenError(msg='字典类型已存在')
            count = await dict_type_dao.update(db, pk, obj)
            return count

    @staticmethod
    async def delete(*, pk: list[int]) -> int:
        async with async_db_session.begin() as db:
            count = await dict_type_dao.delete(db, pk)
            return count


dict_type_service = DictTypeService()
