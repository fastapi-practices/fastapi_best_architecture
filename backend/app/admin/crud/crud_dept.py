#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import and_, asc, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import Dept, User
from backend.app.admin.schema.dept import CreateDeptParam, UpdateDeptParam


class CRUDDept(CRUDPlus[Dept]):
    async def get(self, db: AsyncSession, dept_id: int) -> Dept | None:
        """
        获取部门

        :param db:
        :param dept_id:
        :return:
        """
        return await self.select_model_by_columns(db, id=dept_id, del_flag=0)

    async def get_by_name(self, db: AsyncSession, name: str) -> Dept | None:
        """
        通过 name 获取 API

        :param db:
        :param name:
        :return:
        """
        return await self.select_model_by_columns(db, name=name, del_flag=0)

    async def get_all(
        self, db: AsyncSession, name: str = None, leader: str = None, phone: str = None, status: int = None
    ) -> Sequence[Dept]:
        """
        获取所有部门

        :param db:
        :param name:
        :param leader:
        :param phone:
        :param status:
        :return:
        """
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

    async def create(self, db: AsyncSession, obj_in: CreateDeptParam) -> None:
        """
        创建部门

        :param db:
        :param obj_in:
        :return:
        """
        await self.create_model(db, obj_in)

    async def update(self, db: AsyncSession, dept_id: int, obj_in: UpdateDeptParam) -> int:
        """
        更新部门

        :param db:
        :param dept_id:
        :param obj_in:
        :return:
        """
        return await self.update_model(db, dept_id, obj_in)

    async def delete(self, db: AsyncSession, dept_id: int) -> int:
        """
        删除部门

        :param db:
        :param dept_id:
        :return:
        """
        return await self.delete_model(db, dept_id, del_flag=1)

    async def get_relation(self, db: AsyncSession, dept_id: int) -> list[User]:
        """
        获取关联

        :param db:
        :param dept_id:
        :return:
        """
        result = await db.execute(
            select(self.model).options(selectinload(self.model.users)).where(self.model.id == dept_id)
        )
        user_relation = result.scalars().first()
        return user_relation.users

    async def get_children(self, db: AsyncSession, dept_id: int) -> list[Dept]:
        """
        获取子部门

        :param db:
        :param dept_id:
        :return:
        """
        result = await db.execute(
            select(self.model).options(selectinload(self.model.children)).where(self.model.id == dept_id)
        )
        dept = result.scalars().first()
        return dept.children


dept_dao: CRUDDept = CRUDDept(Dept)
