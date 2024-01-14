#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from datetime import datetime

from fastapi import Request
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models import User


class LoginLogServiceABC(ABC):
    """
    登录日志服务基类
    """

    @abstractmethod
    async def get_select(self, *, username: str, status: int, ip: str) -> Select:
        """
        获取登录日志分页查询

        :param username:
        :param status:
        :param ip:
        :return:
        """
        pass

    @abstractmethod
    async def create(
        self, *, db: AsyncSession, request: Request, user: User, login_time: datetime, status: int, msg: str
    ) -> None:
        """
        创建登录日志

        :param db:
        :param request:
        :param user:
        :param login_time:
        :param status:
        :param msg:
        :return:
        """
        pass

    @abstractmethod
    async def delete(self, *, pk: list[int]) -> int:
        """
        删除登录日志

        :param pk:
        :return:
        """
        pass

    @abstractmethod
    async def delete_all(self) -> int:
        """
        清空登录日志

        :return:
        """
        pass
