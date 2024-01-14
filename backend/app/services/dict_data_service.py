#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from sqlalchemy import Select

from backend.app.models.sys_dict_data import DictData
from backend.app.schemas.dict_data import CreateDictData, UpdateDictData


class DictDataServiceABC(ABC):
    """
    字典数据服务基类
    """

    @abstractmethod
    async def get(self, *, pk: int) -> DictData:
        """
        获取字典数据详情

        :param pk:
        :return:
        """
        pass

    @abstractmethod
    async def get_select(self, *, label: str = None, value: str = None, status: int = None) -> Select:
        """
        获取字典数据分页查询

        :param label:
        :param value:
        :param status:
        :return:
        """
        pass

    @abstractmethod
    async def create(self, *, obj: CreateDictData) -> None:
        """
        创建字典数据

        :param obj:
        :return:
        """
        pass

    @abstractmethod
    async def update(self, *, pk: int, obj: UpdateDictData) -> int:
        """
        更新字典数据

        :param pk:
        :param obj:
        :return:
        """
        pass

    @abstractmethod
    async def delete(self, *, pk: list[int]) -> int:
        """
        删除字典数据

        :param pk:
        :return:
        """
        pass
