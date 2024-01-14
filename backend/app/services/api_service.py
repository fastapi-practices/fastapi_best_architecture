#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Sequence

from sqlalchemy import Select

from backend.app.models import Api
from backend.app.schemas.api import CreateApi, UpdateApi


class ApiServiceABC(ABC):
    """
    后台API信息服务基类
    """

    @abstractmethod
    async def get(self, *, pk: int) -> Api:
        """
        获取API信息详情

        :param pk:
        :return:
        """
        pass

    @abstractmethod
    async def get_select(self, *, name: str = None, method: str = None, path: str = None) -> Select:
        """
        获取API信息分页查询

        :param name:
        :param method:
        :param path:
        :return:
        """
        pass

    @abstractmethod
    async def get_api_list(self) -> Sequence[Api]:
        """
        获取API信息列表

        :return:
        """
        pass

    @abstractmethod
    async def create(self, *, obj: CreateApi) -> None:
        """
        创建API信息

        :param obj:
        :return:
        """
        pass

    @abstractmethod
    async def update(self, *, pk: int, obj: UpdateApi) -> int:
        """
        更新API信息

        :param pk:
        :param obj:
        :return:
        """
        pass

    @abstractmethod
    async def delete(self, *, pk: list[int]) -> int:
        """
        删除API信息

        :param pk:
        :return:
        """
        pass
