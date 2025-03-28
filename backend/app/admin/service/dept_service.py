#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any

from fastapi import Request

from backend.app.admin.crud.crud_dept import dept_dao
from backend.app.admin.model import Dept
from backend.app.admin.schema.dept import CreateDeptParam, UpdateDeptParam
from backend.common.exception import errors
from backend.core.conf import settings
from backend.database.db import async_db_session
from backend.database.redis import redis_client
from backend.utils.build_tree import get_tree_data


class DeptService:
    """部门服务类"""

    @staticmethod
    async def get(*, pk: int) -> Dept:
        """
        获取部门详情

        :param pk: 部门 ID
        :return:
        """
        async with async_db_session() as db:
            dept = await dept_dao.get(db, pk)
            if not dept:
                raise errors.NotFoundError(msg='部门不存在')
            return dept

    @staticmethod
    async def get_dept_tree(
        *, name: str | None = None, leader: str | None = None, phone: str | None = None, status: int | None = None
    ) -> list[dict[str, Any]]:
        """
        获取部门树形结构

        :param name: 部门名称
        :param leader: 部门负责人
        :param phone: 联系电话
        :param status: 状态
        :return:
        """
        async with async_db_session() as db:
            dept_select = await dept_dao.get_all(db=db, name=name, leader=leader, phone=phone, status=status)
            tree_data = get_tree_data(dept_select)
            return tree_data

    @staticmethod
    async def create(*, obj: CreateDeptParam) -> None:
        """
        创建部门

        :param obj: 部门创建参数
        :return:
        """
        async with async_db_session.begin() as db:
            dept = await dept_dao.get_by_name(db, obj.name)
            if dept:
                raise errors.ForbiddenError(msg='部门名称已存在')
            if obj.parent_id:
                parent_dept = await dept_dao.get(db, obj.parent_id)
                if not parent_dept:
                    raise errors.NotFoundError(msg='父级部门不存在')
            await dept_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateDeptParam) -> int:
        """
        更新部门

        :param pk: 部门 ID
        :param obj: 部门更新参数
        :return:
        """
        async with async_db_session.begin() as db:
            dept = await dept_dao.get(db, pk)
            if not dept:
                raise errors.NotFoundError(msg='部门不存在')
            if dept.name != obj.name:
                if await dept_dao.get_by_name(db, obj.name):
                    raise errors.ForbiddenError(msg='部门名称已存在')
            if obj.parent_id:
                parent_dept = await dept_dao.get(db, obj.parent_id)
                if not parent_dept:
                    raise errors.NotFoundError(msg='父级部门不存在')
            if obj.parent_id == dept.id:
                raise errors.ForbiddenError(msg='禁止关联自身为父级')
            count = await dept_dao.update(db, pk, obj)
            return count

    @staticmethod
    async def delete(*, request: Request, pk: int) -> int:
        """
        删除部门

        :param request: FastAPI 请求对象
        :param pk: 部门 ID
        :return:
        """
        async with async_db_session.begin() as db:
            dept = await dept_dao.get_with_relation(db, pk)
            dept_user = dept.users
            if dept_user:
                raise errors.ForbiddenError(msg='部门下存在用户，无法删除')
            children = await dept_dao.get_children(db, pk)
            if children:
                raise errors.ForbiddenError(msg='部门下存在子部门，无法删除')
            count = await dept_dao.delete(db, pk)
            await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{request.user.id}')
            return count


dept_service: DeptService = DeptService()
