#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any

from sqlalchemy import select, and_, asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.crud.base import CRUDBase
from backend.app.models import Dept
from backend.app.schemas.dept import CreateDept, UpdateDept


class CRUDDept(CRUDBase[Dept, CreateDept, UpdateDept]):
    async def get(self, db: AsyncSession, dept_id: int) -> Dept | None:
        return await self.get_(db, pk=dept_id, del_flag=0)

    async def get_by_name(self, db: AsyncSession, name: str) -> Dept | None:
        return await self.get_(db, name=name)

    async def get_all(
        self, db: AsyncSession, name: str = None, leader: str = None, phone: str = None, status: int = None
    ) -> Any:
        se = select(self.model).order_by(asc(self.model.sort))
        where_list = [self.model.del_flag == 0]
        if name:
            where_list.append(self.model.name.like(f'%{name}%'))
        if leader:
            where_list.append(self.model.leader.like(f'%{leader}%'))
        if phone:
            where_list.append(self.model.phone.startswith(phone))
        if status is not None:
            where_list.append(self.model.status == status)
        if where_list:
            se = se.where(and_(*where_list))
        dept = await db.execute(se)
        return dept.scalars().all()

    async def create(self, db: AsyncSession, obj_in: CreateDept) -> None:
        await self.create_(db, obj_in)

    async def update(self, db: AsyncSession, dept_id: int, obj_in: UpdateDept) -> int:
        return await self.update_(db, dept_id, obj_in)

    async def delete(self, db: AsyncSession, dept_id: int) -> int:
        return await self.delete_(db, dept_id, del_flag=1)

    async def get_user_relation(self, db: AsyncSession, dept_id: int) -> Any:
        result = await db.execute(
            select(self.model).options(selectinload(self.model.users)).where(self.model.id == dept_id)
        )
        user_relation = result.scalars().first()
        return user_relation.users

    async def get_children(self, db: AsyncSession, dept_id: int) -> Any:
        result = await db.execute(
            select(self.model).options(selectinload(self.model.children)).where(self.model.id == dept_id)
        )
        dept = result.scalars().first()
        return dept.children


DeptDao: CRUDDept = CRUDDept(Dept)
