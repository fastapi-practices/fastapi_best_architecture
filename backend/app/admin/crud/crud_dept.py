#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from fastapi import Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import Dept
from backend.app.admin.schema.dept import CreateDeptParam, UpdateDeptParam
from backend.common.security.permission import filter_data_permission


class CRUDDept(CRUDPlus[Dept]):
    """Sector database operating class"""

    async def get(self, db: AsyncSession, dept_id: int) -> Dept | None:
        """
        Access to sector details

        :param db: database session
        :param dept_id: Department ID
        :return:
        """
        return await self.select_model_by_column(db, id=dept_id, del_flag=0)

    async def get_by_name(self, db: AsyncSession, name: str) -> Dept | None:
        """
        Acquiring Department by Name

        :param db: database session
        :param name: department name
        :return:
        """
        return await self.select_model_by_column(db, name=name, del_flag=0)

    async def get_all(
        self,
        request: Request,
        db: AsyncSession,
        name: str | None,
        leader: str | None,
        phone: str | None,
        status: int | None,
    ) -> Sequence[Dept]:
        """
        Access to all sectors

        :param request: FastAPI
        :param db: database session
        :param name: department name
        :param leader:
        :param phone:
        :param status: sector status
        :return:
        """
        filters = {'del_flag__eq': 0}
        if name is not None:
            filters.update(name__like=f'%{name}%')
        if leader is not None:
            filters.update(leader__like=f'%{leader}%')
        if phone is not None:
            filters.update(phone__startswith=phone)
        if status is not None:
            filters.update(status=status)
        return await self.select_models_order(db, 'sort', None, await filter_data_permission(db, request), **filters)

    async def create(self, db: AsyncSession, obj: CreateDeptParam) -> None:
        """
        Create Sector

        :param db: database session
        :param obj: create sector parameters
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, dept_id: int, obj: UpdateDeptParam) -> int:
        """
        Update Department

        :param db: database session
        :param dept_id: Department ID
        :param obj: update sector parameters
        :return:
        """
        return await self.update_model(db, dept_id, obj)

    async def delete(self, db: AsyncSession, dept_id: int) -> int:
        """
        Delete Sector

        :param db: database session
        :param dept_id: Department ID
        :return:
        """
        return await self.delete_model_by_column(db, id=dept_id, logical_deletion=True, deleted_flag_column='del_flag')

    async def get_with_relation(self, db: AsyncSession, dept_id: int) -> Dept | None:
        """
        Access to sectoral and associated data

        :param db: database session
        :param dept_id: Department ID
        :return:
        """
        stmt = select(self.model).options(selectinload(self.model.users)).where(self.model.id == dept_id)
        result = await db.execute(stmt)
        return result.scalars().first()

    async def get_children(self, db: AsyncSession, dept_id: int) -> Sequence[Dept | None]:
        """
        Fetch Subsector List

        :param db: database session
        :param dept_id: Department ID
        :return:
        """
        stmt = select(self.model).where(self.model.parent_id == dept_id, self.model.del_flag == 0)
        result = await db.execute(stmt)
        return result.scalars().all()


dept_dao: CRUDDept = CRUDDept(Dept)
