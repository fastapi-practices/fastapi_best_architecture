#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import and_, asc, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.crud.base import CRUDBase
from backend.app.models import Dept, User
from backend.app.schemas.dept import CreateDept, UpdateDept


class CRUDDept(CRUDBase[Dept, CreateDept, UpdateDept]):
    async def get(self, db: AsyncSession, dept_id: int) -> Dept | None:
        return await self.get_(db, pk=dept_id, del_flag=0)

    async def get_by_name(self, db: AsyncSession, name: str) -> Dept | None:
        return await self.get_(db, name=name, del_flag=0)

    async def get_all(
        self, db: AsyncSession, name: str = None, leader: str = None, phone: str = None, status: int = None
    ) -> Sequence[Dept]:
        se = select(self.model).order_by(asc(self.model.sort))
        where_list = [self.model.del_flag == 0]
        conditions = []
        if name:
            conditions.append(self.model.name.like(f'%{name}%'))
        if leader:
            conditions.append(self.model.leader.like(f'%{leader}%'))
        if phone:
            se_phone = self.model.phone.startswith(phone)
            dept_select = await db.execute(se.where(se_phone))
            dept_likes = dept_select.scalars().all()
            where_list.append(or_(se_phone, self.model.id.in_([dept.parent_id for dept in dept_likes])))
        if status is not None:
            where_list.append(self.model.status == status)
        if conditions:
            dept_select = await db.execute(se.where(and_(*conditions)))
            dept_likes = dept_select.scalars().all()
            where_list.append(or_(*conditions, self.model.id.in_([dept.parent_id for dept in dept_likes])))
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

    async def get_user_relation(self, db: AsyncSession, dept_id: int) -> list[User]:
        result = await db.execute(
            select(self.model).options(selectinload(self.model.users)).where(self.model.id == dept_id)
        )
        user_relation = result.scalars().first()
        return user_relation.users

    async def get_children(self, db: AsyncSession, dept_id: int) -> list[Dept]:
        result = await db.execute(
            select(self.model).options(selectinload(self.model.children)).where(self.model.id == dept_id)
        )
        dept = result.scalars().first()
        return dept.children


DeptDao: CRUDDept = CRUDDept(Dept)
