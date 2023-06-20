#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select

from backend.app.common.exception import errors
from backend.app.crud.crud_dict_type import DictTypeDao
from backend.app.database.db_mysql import async_db_session
from backend.app.schemas.dict_type import CreateDictType, UpdateDictType


class DictTypeService:
    @staticmethod
    async def get_select(*, name: str = None, code: str = None, status: int = None) -> Select:
        return await DictTypeDao.get_all(name=name, code=code, status=status)

    @staticmethod
    async def create(*, obj: CreateDictType) -> None:
        async with async_db_session.begin() as db:
            dict_type = await DictTypeDao.get_by_code(db, obj.code)
            if dict_type:
                raise errors.ForbiddenError(msg='字典类型已存在')
            await DictTypeDao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateDictType) -> int:
        async with async_db_session.begin() as db:
            dict_type = await DictTypeDao.get(db, pk)
            if not dict_type:
                raise errors.NotFoundError(msg='字典类型不存在')
            if dict_type.code != obj.code:
                if await DictTypeDao.get_by_code(db, obj.code):
                    raise errors.ForbiddenError(msg='字典类型已存在')
            count = await DictTypeDao.update(db, pk, obj)
            return count

    @staticmethod
    async def delete(*, pk: list[int]) -> int:
        async with async_db_session.begin() as db:
            count = await DictTypeDao.delete(db, pk)
            return count
