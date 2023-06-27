#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import select, asc, and_

from backend.app.crud.base import CRUDBase
from backend.app.models import Menu
from backend.app.schemas.menu import CreateMenu, UpdateMenu


class CRUDMenu(CRUDBase[Menu, CreateMenu, UpdateMenu]):
    async def get(self, db, menu_id: int) -> Menu | None:
        return await self.get_(db, pk=menu_id)

    async def get_by_name(self, db, name: str) -> Menu | None:
        return await self.get_(db, name=name)

    async def get_all(self, db, name: str | None = None, status: int | None = None) -> list[Menu]:
        se = select(self.model).order_by(asc(self.model.sort))
        where_list = []
        if name:
            where_list.append(self.model.name.like(f'%{name}%'))
        if status is not None:
            where_list.append(self.model.status == status)
        if where_list:
            se = se.where(and_(*where_list))
        menu = await db.execute(se)
        return menu.scalars().all()

    async def get_role_menus(self, db, menu_ids: list[int]) -> list[Menu]:
        se = (
            select(self.model)
            .where(self.model.id.in_(menu_ids))
            .where(self.model.status == 1)
            .order_by(asc(self.model.sort))
        )
        menu = await db.execute(se)
        return menu.scalars().all()

    async def create(self, db, obj_in: CreateMenu) -> None:
        await self.create_(db, obj_in)

    async def update(self, db, menu_id: int, obj_in: UpdateMenu) -> int:
        return await self.update_(db, menu_id, obj_in)

    async def delete(self, db, menu_id: int) -> int:
        return await self.delete_(db, menu_id)

    async def get_children(self, db, menu_id: int) -> list[Menu]:
        result = await db.execute(select(self.model).where(self.model.id == menu_id))
        menu = result.scalars().first()
        return menu.children


MenuDao: CRUDMenu = CRUDMenu(Menu)
