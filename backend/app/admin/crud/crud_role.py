#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select, delete, desc, select
from sqlalchemy.orm import selectinload
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import Menu, Role, User
from backend.app.admin.schema.role import CreateRoleParam, UpdateRoleMenuParam, UpdateRoleParam


class CRUDRole(CRUDPlus[Role]):
    async def get(self, db, role_id: int) -> Role | None:
        """
        获取角色

        :param db:
        :param role_id:
        :return:
        """
        return await self.select_model_by_id(db, role_id)

    async def get_with_relation(self, db, role_id: int) -> Role | None:
        """
        获取角色和菜单

        :param db:
        :param role_id:
        :return:
        """
        role = await db.execute(
            select(self.model).options(selectinload(self.model.menus)).where(self.model.id == role_id)
        )
        return role.scalars().first()

    async def get_all(self, db) -> Sequence[Role]:
        """
        获取所有角色

        :param db:
        :return:
        """
        return await self.select_models(db)

    async def get_user_roles(self, db, user_id: int) -> Sequence[Role]:
        """
        获取用户所有角色

        :param db:
        :param user_id:
        :return:
        """
        roles = await db.execute(select(self.model).join(self.model.users).where(User.id == user_id))
        return roles.scalars().all()

    async def get_list(self, name: str = None, data_scope: int = None, status: int = None) -> Select:
        """
        获取角色列表

        :param name:
        :param data_scope:
        :param status:
        :return:
        """
        se = select(self.model).options(selectinload(self.model.menus)).order_by(desc(self.model.created_time))
        where_list = []
        if name:
            where_list.append(self.model.name.like(f'%{name}%'))
        if data_scope:
            where_list.append(self.model.data_scope == data_scope)
        if status is not None:
            where_list.append(self.model.status == status)
        if where_list:
            se = se.where(*where_list)
        return se

    async def get_by_name(self, db, name: str) -> Role | None:
        """
        通过 name 获取角色

        :param db:
        :param name:
        :return:
        """
        return await self.select_model_by_column(db, 'name', name)

    async def create(self, db, obj_in: CreateRoleParam) -> None:
        """
        创建角色

        :param db:
        :param obj_in:
        :return:
        """
        await self.create_model(db, obj_in)

    async def update(self, db, role_id: int, obj_in: UpdateRoleParam) -> int:
        """
        更新角色

        :param db:
        :param role_id:
        :param obj_in:
        :return:
        """
        rowcount = await self.update_model(db, role_id, obj_in)
        return rowcount

    async def update_menus(self, db, role_id: int, menu_ids: UpdateRoleMenuParam) -> int:
        """
        更新角色菜单

        :param db:
        :param role_id:
        :param menu_ids:
        :return:
        """
        current_role = await self.get_with_relation(db, role_id)
        # 更新菜单
        menus = await db.execute(select(Menu).where(Menu.id.in_(menu_ids.menus)))
        current_role.menus = menus.scalars().all()
        return len(current_role.menus)

    async def delete(self, db, role_id: list[int]) -> int:
        """
        删除角色

        :param db:
        :param role_id:
        :return:
        """
        roles = await db.execute(delete(self.model).where(self.model.id.in_(role_id)))
        return roles.rowcount


role_dao: CRUDRole = CRUDRole(Role)
