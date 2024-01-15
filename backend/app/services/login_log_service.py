#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from datetime import datetime

from fastapi import Request
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.common.log import log
from backend.app.crud.crud_login_log import LoginLogDao
from backend.app.database.db_mysql import async_db_session
from backend.app.models import User
from backend.app.schemas.login_log import CreateLoginLog


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


class LoginLogServiceImpl(LoginLogServiceABC):
    """
    登录日志服务实现类
    """

    async def get_select(self, *, username: str, status: int, ip: str) -> Select:
        return await LoginLogDao.get_all(username=username, status=status, ip=ip)

    async def create(
        self, *, db: AsyncSession, request: Request, user: User, login_time: datetime, status: int, msg: str
    ) -> None:
        try:
            # request.state 来自 opera log 中间件定义的扩展参数，详见 opera_log_middleware.py
            obj_in = CreateLoginLog(
                user_uuid=user.uuid,
                username=user.username,
                status=status,
                ip=request.state.ip,
                country=request.state.country,
                region=request.state.region,
                city=request.state.city,
                user_agent=request.state.user_agent,
                browser=request.state.browser,
                os=request.state.os,
                device=request.state.device,
                msg=msg,
                login_time=login_time,
            )
            await LoginLogDao.create(db, obj_in)
        except Exception as e:
            log.exception(f'登录日志创建失败: {e}')

    async def delete(self, *, pk: list[int]) -> int:
        async with async_db_session.begin() as db:
            count = await LoginLogDao.delete(db, pk)
            return count

    async def delete_all(self) -> int:
        async with async_db_session.begin() as db:
            count = await LoginLogDao.delete_all(db)
            return count


LoginLogService: LoginLogServiceABC = LoginLogServiceImpl()
