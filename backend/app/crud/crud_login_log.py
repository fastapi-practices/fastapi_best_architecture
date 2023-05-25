#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import NoReturn

from sqlalchemy import Select, select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.crud.base import CRUDBase
from backend.app.models import LoginLog
from backend.app.schemas.login_log import CreateLoginLog, UpdateLoginLog


class CRUDLoginLog(CRUDBase[LoginLog, CreateLoginLog, UpdateLoginLog]):
    async def create(self, db: AsyncSession, obj_in: CreateLoginLog) -> NoReturn:
        await self.create_(db, obj_in)
        await db.commit()

    async def get_all(self) -> Select:
        return select(self.model).order_by(desc(self.model.create_time))


LoginLogDao: CRUDLoginLog = CRUDLoginLog(LoginLog)
