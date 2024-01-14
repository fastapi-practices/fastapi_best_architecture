#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select

from backend.app.common.exception import errors
from backend.app.crud.crud_dict_data import DictDataDao
from backend.app.crud.crud_dict_type import DictTypeDao
from backend.app.database.db_mysql import async_db_session
from backend.app.models.sys_dict_data import DictData
from backend.app.schemas.dict_data import CreateDictData, UpdateDictData
from backend.app.services.dict_data_service import DictDataServiceABC


class DictDataServiceImpl(DictDataServiceABC):
    async def get(self, *, pk: int) -> DictData:
        async with async_db_session() as db:
            dict_data = await DictDataDao.get_with_relation(db, pk)
            if not dict_data:
                raise errors.NotFoundError(msg='字典数据不存在')
            return dict_data

    async def get_select(self, *, label: str = None, value: str = None, status: int = None) -> Select:
        return await DictDataDao.get_all(label=label, value=value, status=status)

    async def create(self, *, obj: CreateDictData) -> None:
        async with async_db_session.begin() as db:
            dict_data = await DictDataDao.get_by_label(db, obj.label)
            if dict_data:
                raise errors.ForbiddenError(msg='字典数据已存在')
            dict_type = await DictTypeDao.get(db, obj.type_id)
            if not dict_type:
                raise errors.ForbiddenError(msg='字典类型不存在')
            await DictDataDao.create(db, obj)

    async def update(self, *, pk: int, obj: UpdateDictData) -> int:
        async with async_db_session.begin() as db:
            dict_data = await DictDataDao.get(db, pk)
            if not dict_data:
                raise errors.NotFoundError(msg='字典数据不存在')
            if dict_data.label != obj.label:
                if await DictDataDao.get_by_label(db, obj.label):
                    raise errors.ForbiddenError(msg='字典数据已存在')
            dict_type = await DictTypeDao.get(db, obj.type_id)
            if not dict_type:
                raise errors.ForbiddenError(msg='字典类型不存在')
            count = await DictDataDao.update(db, pk, obj)
            return count

    async def delete(self, *, pk: list[int]) -> int:
        async with async_db_session.begin() as db:
            count = await DictDataDao.delete(db, pk)
            return count


DictDateService = DictDataServiceImpl()
