#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import and_, asc, select
from sqlalchemy.orm import selectinload

from backend.app.crud.base import CRUDBase
from backend.app.models import Menu
from backend.app.schemas.menu import CreateMenu, UpdateMenu


class CRUDMenu(CRUDBase[Menu, CreateMenu, UpdateMenu]):
    async def get(self, db, menu_id: int) -> Menu | None:
        return await self.get_(db, pk=menu_id)

    async def get_by_title(self, db, title: str) -> Menu | None:
        result = await db.execute(select(self.model).where(and_(self.model.title == title, self.model.menu_type != 2)))
        return result.scalars().first()

    async def get_all(self, db, title: str | None = None, status: int | None = None) -> Sequence[Menu]:
        se = select(self.model).order_by(asc(self.model.sort))
        where_list = []
        if title:
            where_list.append(self.model.title.like(f'%{title}%'))
        if status is not None:
            where_list.append(self.model.status == status)
        if where_list:
            se = se.where(and_(*where_list))
        menu = await db.execute(se)
        return menu.scalars().all()

    async def get_role_menus(self, db, superuser: bool, menu_ids: list[int]) -> Sequence[Menu]:
        se = select(self.model).order_by(asc(self.model.sort))
        where_list = [self.model.menu_type.in_([0, 1])]
        if not superuser:
            where_list.append(self.model.id.in_(menu_ids))
        se = se.where(and_(*where_list))
        menu = await db.execute(se)
        return menu.scalars().all()

    async def create(self, db, obj_in: CreateMenu) -> None:
        await self.create_(db, obj_in)

    async def update(self, db, menu_id: int, obj_in: UpdateMenu) -> int:
        count = await self.update_(db, menu_id, obj_in)
        return count

    async def delete(self, db, menu_id: int) -> int:
        return await self.delete_(db, menu_id)

    async def get_children(self, db, menu_id: int) -> list[Menu]:
        result = await db.execute(
            select(self.model).options(selectinload(self.model.children)).where(self.model.id == menu_id)
        )
        menu = result.scalars().first()
        return menu.children


MenuDao: CRUDMenu = CRUDMenu(Menu)
