#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from sqlalchemy import Select

from backend.app.common.exception import errors
from backend.app.crud.crud_dict_type import DictTypeDao
from backend.app.database.db_mysql import async_db_session
from backend.app.schemas.dict_type import CreateDictType, UpdateDictType


class DictTypeServiceABC(ABC):
    """
    字典类型服务基类
    """

    @abstractmethod
    async def get_select(self, *, name: str = None, code: str = None, status: int = None) -> Select:
        """
        获取字典类型分页查询

        :param name:
        :param code:
        :param status:
        :return:
        """
        pass

    @abstractmethod
    async def create(self, *, obj: CreateDictType) -> None:
        """
        创建字典类型

        :param obj:
        :return:
        """
        pass

    @abstractmethod
    async def update(self, *, pk: int, obj: UpdateDictType) -> int:
        """
        更新字典类型

        :param pk:
        :param obj:
        :return:
        """
        pass

    @abstractmethod
    async def delete(self, *, pk: list[int]) -> int:
        """
        删除字典类型

        :param pk:
        :return:
        """
        pass


class DictTypeServiceImpl(DictTypeServiceABC):
    """
    字典类型服务实现类
    """

    async def get_select(self, *, name: str = None, code: str = None, status: int = None) -> Select:
        return await DictTypeDao.get_all(name=name, code=code, status=status)

    async def create(self, *, obj: CreateDictType) -> None:
        async with async_db_session.begin() as db:
            dict_type = await DictTypeDao.get_by_code(db, obj.code)
            if dict_type:
                raise errors.ForbiddenError(msg='字典类型已存在')
            await DictTypeDao.create(db, obj)

    async def update(self, *, pk: int, obj: UpdateDictType) -> int:
        async with async_db_session.begin() as db:
            dict_type = await DictTypeDao.get(db, pk)
            if not dict_type:
                raise errors.NotFoundError(msg='字典类型不存在')
            if dict_type.code != obj.code:
                if await DictTypeDao.get_by_code(db, obj.code):
                    raise errors.ForbiddenError(msg='字典类型已存在')
            count = await DictTypeDao.update(db, pk, obj)
            return count

    async def delete(self, *, pk: list[int]) -> int:
        async with async_db_session.begin() as db:
            count = await DictTypeDao.delete(db, pk)
            return count


DictTypeService: DictTypeServiceABC = DictTypeServiceImpl()
