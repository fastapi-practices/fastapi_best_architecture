#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import NoReturn

from fastapi import Request
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from user_agents import parse

from backend.app.common.log import log
from backend.app.core.conf import settings
from backend.app.crud.crud_login_log import LoginLogDao
from backend.app.database.db_mysql import async_db_session
from backend.app.models import User
from backend.app.schemas.login_log import CreateLoginLog
from backend.app.utils import request_parse


class LoginLogService:
    @staticmethod
    async def get_select() -> Select:
        return await LoginLogDao.get_all()

    @staticmethod
    async def create(
        *, db: AsyncSession, request: Request, user: User, login_time: datetime, status: int, msg: str
    ) -> NoReturn:
        try:
            ip = await request_parse.get_request_ip(request)
            user_agent = request.headers.get('User-Agent')
            _, os_info, browser = str(parse(user_agent)).replace(' ', '').split('/')
            if settings.LOCATION_PARSE == 'online':
                location = await request_parse.get_location_online(ip, user_agent)
            elif settings.LOCATION_PARSE == 'offline':
                location = request_parse.get_location_offline(ip)
            else:
                location = '未知'
            obj_in = CreateLoginLog(
                user_uuid=user.user_uuid,
                username=user.username,
                status=status,
                ipaddr=ip,
                location=location,
                browser=browser,
                os=os_info,
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
