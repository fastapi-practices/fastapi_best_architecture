#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.crud.crud_login_log import LoginLogDao
from backend.app.schemas.login_log import CreateLoginLog


class LoginLogService:

    @staticmethod
    async def get_select():
        return await LoginLogDao.get_all()

    @staticmethod
    async def create(db: AsyncSession, obj_in: CreateLoginLog):
        await LoginLogDao.create(db, obj_in)
