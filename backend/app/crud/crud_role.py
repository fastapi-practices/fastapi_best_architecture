#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import NoReturn

from sqlalchemy import select, delete, desc
from sqlalchemy.orm import selectinload

from backend.app.crud.base import CRUDBase
from backend.app.models import Role, Menu, User
from backend.app.schemas.role import CreateRole, UpdateRole


class CRUDRole(CRUDBase[Role, CreateRole, UpdateRole]):
    async def get(self, db, role_id: int) -> Role | None:
        return await self.get_(db, pk=role_id)

    async def get_with_relation(self, db, role_id: int) -> Role | None:
        role = await db.execute(
            select(self.model).options(selectinload(self.model.menus)).where(self.model.id == role_id)
        )
        return role.scalars().first()

    async def get_all(self, db) -> list[Role]:
        roles = await db.execute(select(self.model))
        return roles.scalars().all()

    async def get_user_all(self, db, user_id: int) -> list[Role]:
        roles = await db.execute(select(self.model).join(self.model.users).where(User.id == user_id))
        return roles.scalars().all()

    async def get_list(self, name: str = None, data_scope: int = None):
        se = select(self.model).options(selectinload(self.model.menus)).order_by(desc(self.model.created_time))
        where_list = []
        if name:
            where_list.append(self.model.name.like(f'%{name}%'))
        if data_scope:
            where_list.append(self.model.data_scope == data_scope)
        if where_list:
            se = se.where(*where_list)
        return se

    async def get_by_name(self, db, name: str) -> Role | None:
        role = await db.execute(select(self.model).where(self.model.name == name))
        return role.scalars().first()

    async def create(self, db, obj_in: CreateRole) -> NoReturn:
        await self.create_(db, obj_in)

    async def update(self, db, role_id: int, obj_in: UpdateRole) -> int:
        rowcount = await self.update_(db, pk=role_id, obj_in=obj_in)
        return rowcount

    async def update_menus(self, db, role_id: int, menu_ids: list[int]) -> int:
        current_role = await self.get_with_relation(db, role_id)
        # 更新菜单
        menus = await db.execute(select(Menu).where(Menu.id.in_(menu_ids)))
        current_role.menus = menus.scalars().all()
        return len(current_role.menus)

    async def delete(self, db, role_id: list[int]) -> int:
        roles = await db.execute(delete(self.model).where(self.model.id.in_(role_id)))
        return roles.rowcount


RoleDao: CRUDRole = CRUDRole(Role)
