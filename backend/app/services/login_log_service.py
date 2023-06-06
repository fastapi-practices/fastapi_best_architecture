#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import NoReturn

from fastapi import Request
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.common.log import log
from backend.app.crud.crud_login_log import LoginLogDao
from backend.app.database.db_mysql import async_db_session
from backend.app.models import User
from backend.app.schemas.login_log import CreateLoginLog
from backend.app.utils import request_parse


class LoginLogService:
    @staticmethod
    async def get_select(*, username: str, status: bool, ipaddr: str) -> Select:
        return await LoginLogDao.get_all(username=username, status=status, ipaddr=ipaddr)

    @staticmethod
    async def create(
        *, db: AsyncSession, request: Request, user: User, login_time: datetime, status: bool, msg: str
    ) -> NoReturn:
        try:
            ip = await request_parse.get_request_ip(request)
            # 来自 opera log 中间件定义的扩展参数，详见 opera_log_middleware.py
            location = request.state.location
            browser = request.state.browser
            os = request.state.os
            obj_in = CreateLoginLog(
                user_uuid=user.user_uuid,
                username=user.username,
                status=status,
                ipaddr=ip,
                location=location,
                browser=browser,
                os=os,
                msg=msg,
                login_time=login_time,
            )
            await LoginLogDao.create(db, obj_in)
        except Exception as e:
            log.exception(f'登录日志创建失败: {e}')

    @staticmethod
    async def delete(pk: list[int]) -> int:
        async with async_db_session.begin() as db:
            count = await LoginLogDao.delete(db, pk)
            return count

    @staticmethod
    async def delete_all() -> int:
        async with async_db_session.begin() as db:
            count = await LoginLogDao.delete_all(db)
            return count
