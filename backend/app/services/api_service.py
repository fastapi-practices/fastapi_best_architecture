#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select

from backend.app.common.exception import errors
from backend.app.crud.crud_api import ApiDao
from backend.app.database.db_mysql import async_db_session
from backend.app.models import Api
from backend.app.schemas.api import CreateApi, UpdateApi


class ApiService:
    @staticmethod
    async def get(*, pk: int) -> Api:
        async with async_db_session() as db:
            api = await ApiDao.get(db, pk)
            if not api:
                raise errors.NotFoundError(msg='接口不存在')
            return api

    @staticmethod
    async def get_select(*, name: str = None, method: str = None, path: str = None) -> Select:
        return await ApiDao.get_all(name=name, method=method, path=path)

    @staticmethod
    async def create(*, obj: CreateApi, user_id: int) -> None:
        async with async_db_session.begin() as db:
            api = await ApiDao.get_by_name(db, obj.name)
            if api:
                raise errors.ForbiddenError(msg='接口已存在')
            await ApiDao.create(db, obj, user_id)

    @staticmethod
    async def update(*, pk: int, obj: UpdateApi, user_id: int) -> int:
        async with async_db_session.begin() as db:
            count = await ApiDao.update(db, pk, obj, user_id)
            return count

    @staticmethod
    async def delete(*, pk: list[int]) -> int:
        async with async_db_session.begin() as db:
            count = await ApiDao.delete(db, pk)
            return count
