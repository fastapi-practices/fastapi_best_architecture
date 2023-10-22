#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any

from backend.app.common.exception import errors
from backend.app.crud.crud_dept import DeptDao
from backend.app.database.db_mysql import async_db_session
from backend.app.models import Dept
from backend.app.schemas.dept import CreateDept, UpdateDept
from backend.app.utils.build_tree import get_tree_data


class DeptService:
    @staticmethod
    async def get(*, pk: int) -> Dept:
        async with async_db_session() as db:
            dept = await DeptDao.get(db, pk)
            if not dept:
                raise errors.NotFoundError(msg='部门不存在')
            return dept

    @staticmethod
    async def get_dept_tree(
        *, name: str | None = None, leader: str | None = None, phone: str | None = None, status: int | None = None
    ) -> list[dict[str, Any]]:
        async with async_db_session() as db:
            dept_select = await DeptDao.get_all(db=db, name=name, leader=leader, phone=phone, status=status)
            tree_data = await get_tree_data(dept_select)
            return tree_data

    @staticmethod
    async def create(*, obj: CreateDept) -> None:
        async with async_db_session.begin() as db:
            dept = await DeptDao.get_by_name(db, obj.name)
            if dept:
                raise errors.ForbiddenError(msg='部门名称已存在')
            if obj.parent_id:
                parent_dept = await DeptDao.get(db, obj.parent_id)
                if not parent_dept:
                    raise errors.NotFoundError(msg='父级部门不存在')
            await DeptDao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateDept) -> int:
        async with async_db_session.begin() as db:
            dept = await DeptDao.get(db, pk)
            if not dept:
                raise errors.NotFoundError(msg='部门不存在')
            if dept.name != obj.name:
                if await DeptDao.get_by_name(db, obj.name):
                    raise errors.ForbiddenError(msg='部门名称已存在')
            if obj.parent_id:
                parent_dept = await DeptDao.get(db, obj.parent_id)
                if not parent_dept:
                    raise errors.NotFoundError(msg='父级部门不存在')
            count = await DeptDao.update(db, pk, obj)
            return count

    @staticmethod
    async def delete(*, pk: int) -> int:
        async with async_db_session.begin() as db:
            dept_user = await DeptDao.get_user_relation(db, pk)
            if dept_user:
                raise errors.ForbiddenError(msg='部门下存在用户，无法删除')
            children = await DeptDao.get_children(db, pk)
            if children:
                raise errors.ForbiddenError(msg='部门下存在子部门，无法删除')
            count = await DeptDao.delete(db, pk)
            return count
