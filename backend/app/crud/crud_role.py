#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import NoReturn

from sqlalchemy import select, update, delete, desc
from sqlalchemy.orm import selectinload

from backend.app.crud.base import CRUDBase
from backend.app.models import Role, Menu
from backend.app.schemas.role import CreateRole, UpdateRole


class CRUDRole(CRUDBase[Role, CreateRole, UpdateRole]):
    async def get(self, db, role_id: int) -> Role | None:
        return await self.get_(db, pk=role_id)

    async def get_with_relation(self, db, role_id: int) -> Role | None:
        role = await db.execute(
            select(self.model).options(selectinload(self.model.menus)).where(self.model.id == role_id)
        )
        return role.scalars().first()

    async def get_all(self, name: str = None, data_scope: int = None):
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
        new_role = self.model(**obj_in.dict(exclude={'menus'}))
        menu_list = []
        for menu_id in obj_in.menus:
            menu_list.append(await db.get(Menu, menu_id))
        new_role.menus.append(*menu_list)
        db.add(new_role)

    async def update(self, db, role_id: int, obj_in: UpdateRole) -> int:
        role = await db.execute(
            update(self.model).where(self.model.id == role_id).values(**obj_in.dict(exclude={'menus'}))
        )
        current_role = await self.get_with_relation(db, role_id)
        # 删除角色所有菜单
        for i in list(current_role.menus):
            current_role.menus.remove(i)
        # 添加角色菜单
        menu_list = []
        for menu_id in obj_in.menus:
            menu_list.append(await db.get(Menu, menu_id))
        current_role.menus.append(*menu_list)
        return role.rowcount

    async def delete(self, db, role_id: list[int]) -> int:
        roles = await db.execute(delete(self.model).where(self.model.id.in_(role_id)))
        return roles.rowcount


RoleDao: CRUDRole = CRUDRole(Role)
