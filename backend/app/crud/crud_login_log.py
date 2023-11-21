#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select, and_, delete, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.crud.base import CRUDBase
from backend.app.models import LoginLog
from backend.app.schemas.login_log import CreateLoginLog, UpdateLoginLog


class CRUDLoginLog(CRUDBase[LoginLog, CreateLoginLog, UpdateLoginLog]):
    async def get_all(self, username: str | None = None, status: int | None = None, ip: str | None = None) -> Select:
        se = select(self.model).order_by(desc(self.model.created_time))
        where_list = []
        if username:
            where_list.append(self.model.username.like(f'%{username}%'))
        if status is not None:
            where_list.append(self.model.status == status)
        if ip:
            where_list.append(self.model.ip.like(f'%{ip}%'))
        if where_list:
            se = se.where(and_(*where_list))
        return se

    async def create(self, db: AsyncSession, obj_in: CreateLoginLog):
        await self.create_(db, obj_in)
        await db.commit()

    async def delete(self, db: AsyncSession, pk: list[int]) -> int:
        logs = await db.execute(delete(self.model).where(self.model.id.in_(pk)))
        return logs.rowcount

    async def delete_all(self, db: AsyncSession) -> int:
        logs = await db.execute(delete(self.model))
        return logs.rowcount


LoginLogDao: CRUDLoginLog = CRUDLoginLog(LoginLog)
