#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from sqlalchemy import Select

from backend.app.schemas.opera_log import CreateOperaLog


class OperaLogServiceABC(ABC):
    """
    操作日志服务基类
    """

    @abstractmethod
    async def get_select(
        self, *, username: str | None = None, status: int | None = None, ip: str | None = None
    ) -> Select:
        """
        获取操作日志分页查询

        :param username:
        :param status:
        :param ip:
        :return:
        """
        pass

    @abstractmethod
    async def create(self, *, obj_in: CreateOperaLog) -> None:
        """
        创建分页日志

        :param obj_in:
        :return:
        """
        pass

    @abstractmethod
    async def delete(self, *, pk: list[int]) -> int:
        """
        删除分页日志

        :param pk:
        :return:
        """
        pass

    @abstractmethod
    async def delete_all(self) -> int:
        """
        清空分页日志

        :return:
        """
        pass
