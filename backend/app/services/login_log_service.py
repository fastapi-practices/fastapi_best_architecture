#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from fastapi import Request
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.common.log import log
from backend.app.crud.crud_login_log import LoginLogDao
from backend.app.database.db_mysql import async_db_session
from backend.app.models import User
from backend.app.schemas.login_log import CreateLoginLog
from backend.app.utils.request_parse import parse_user_agent_info, parse_ip_info


class LoginLogService:
    @staticmethod
    async def get_select(*, username: str, status: int, ip: str) -> Select:
        return await LoginLogDao.get_all(username=username, status=status, ip=ip)

    @staticmethod
    async def create(
        *, db: AsyncSession, request: Request, user: User, login_time: datetime, status: int, msg: str
    ) -> None:
        try:
            # request.state 来自 opera log 中间件定义的扩展参数，详见 opera_log_middleware.py
            user_agent, device, os, browser = await parse_user_agent_info(request)
            ip, country, region, city = await parse_ip_info(request)
            obj_in = CreateLoginLog(
                user_uuid=user.uuid,
                username=user.username,
                status=status,
                ip=ip,
                country=country,
                region=region,
                city=city,
                user_agent=user_agent,
                browser=browser,
                os=os,
                device=device,
                msg=msg,
                login_time=login_time,
            )
            await LoginLogDao.create(db, obj_in)
        except Exception as e:
            log.exception(f'登录日志创建失败: {e}')

    @staticmethod
    async def delete(*, pk: list[int]) -> int:
        async with async_db_session.begin() as db:
            count = await LoginLogDao.delete(db, pk)
            return count

    @staticmethod
    async def delete_all() -> int:
        async with async_db_session.begin() as db:
            count = await LoginLogDao.delete_all(db)
            return count
