#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select

from backend.app.common.exception import errors
from backend.app.crud.crud_api import api_dao
from backend.app.database.db_mysql import async_db_session
from backend.app.models import Api
from backend.app.schemas.api import CreateApiParam, UpdateApiParam


class ApiService:
    @staticmethod
    async def get(*, pk: int) -> Api:
        async with async_db_session() as db:
            api = await api_dao.get(db, pk)
            if not api:
                raise errors.NotFoundError(msg='接口不存在')
            return api

    @staticmethod
    async def get_select(*, name: str = None, method: str = None, path: str = None) -> Select:
        return await api_dao.get_list(name=name, method=method, path=path)

    @staticmethod
    async def get_api_list() -> Sequence[Api]:
        async with async_db_session() as db:
            apis = await api_dao.get_all(db)
            return apis

    @staticmethod
    async def create(*, obj: CreateApiParam) -> None:
        async with async_db_session.begin() as db:
            api = await api_dao.get_by_name(db, obj.name)
            if api:
                raise errors.ForbiddenError(msg='接口已存在')
            await api_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateApiParam) -> int:
        async with async_db_session.begin() as db:
            count = await api_dao.update(db, pk, obj)
            return count

    @staticmethod
    async def delete(*, pk: list[int]) -> int:
        async with async_db_session.begin() as db:
            count = await api_dao.delete(db, pk)
            return count


api_service: ApiService = ApiService()
