#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from sqlalchemy import Select

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
