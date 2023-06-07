#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import event

from backend.app.common.exception import errors
from backend.app.crud.crud_dept import DeptDao
from backend.app.database.db_mysql import async_db_session
from backend.app.models import Dept
from backend.app.schemas.dept import CreateDept, UpdateDept
from backend.app.utils.build_tree import get_tree_data


class DeptService:
    @staticmethod
    async def get(*, pk: int):
        async with async_db_session() as db:
            dept = await DeptDao.get(db, pk)
            if not dept:
                raise errors.NotFoundError(msg='部门不存在')
            if not dept.status:
                raise errors.ForbiddenError(msg='部门已关停')
            return dept

    @staticmethod
    async def get_select(
        *, name: str | None = None, leader: str | None = None, phone: str | None = None, status: bool | None = None
    ):
        async with async_db_session() as db:
            dept_select = await DeptDao.get_all(db=db, name=name, leader=leader, phone=phone, status=status)
            tree_data = await get_tree_data(dept_select)
            return tree_data

    @staticmethod
    async def create(*, obj: CreateDept, user_id: int):
        async with async_db_session() as db:
            dept = await DeptDao.get(db, user_id)
            if dept.name == obj.name:
                raise errors.ForbiddenError(msg='部门名称已存在')
            new_obj = obj.dict()
            new_obj.update({'level': obj.parent_id + 1 if obj.parent_id else 1, 'create_user': user_id})
            await DeptDao.create(db, new_obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateDept, user_id: int):
        async with async_db_session() as db:
            dept = await DeptDao.get(db, pk)
            if dept.name == obj.name:
                raise errors.ForbiddenError(msg='部门名称已存在')
            new_obj = obj.dict()
            new_obj.update({'level': obj.parent_id + 1 if obj.parent_id else 1, 'update_user': user_id})
            count = await DeptDao.update(db, pk, new_obj)
            return count

    @staticmethod
    async def delete(*, pk: int):
        async with async_db_session() as db:
            dept_user = await DeptDao.get_user_relation(db, pk)
            if dept_user:
                # 用于确认监听事件是否生效
                raise errors.ForbiddenError(msg='部门下存在用户，无法删除')
            children = await DeptDao.get_children(db, pk)
            if children:
                raise errors.ForbiddenError(msg='部门下存在子部门，无法删除')
            count = await DeptDao.delete(db, pk)
            return count

    @staticmethod
    @event.listens_for(Dept, 'before_delete')
    async def before_delete_handler(dept_id: int):
        async with async_db_session() as db:
            await DeptDao.remove_user_relation(db, dept_id)
