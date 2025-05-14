#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import and_, asc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import Menu
from backend.app.admin.schema.menu import CreateMenuParam, UpdateMenuParam


class CRUDMenu(CRUDPlus[Menu]):
    """Menu Database Operations Category"""

    async def get(self, db: AsyncSession, menu_id: int) -> Menu | None:
        """
        Get Menu Details

        :param db: database session
        :param menu_id: menu ID
        :return:
        """
        return await self.select_model(db, menu_id)

    async def get_by_title(self, db: AsyncSession, title: str) -> Menu | None:
        """
        Get Menu Through Title

        :param db: database session
        :param type: menu title
        :return:
        """
        return await self.select_model_by_column(db, title=title, type__ne=2)

    async def get_all(self, db: AsyncSession, title: str | None, status: int | None) -> Sequence[Menu]:
        """
        Get Menu List

        :param db: database session
        :param type: menu title
        :param status: menu status
        :return:
        """
        filters = {}
        if title is not None:
            filters.update(title=f'%{title}%')
        if status is not None:
            filters.update(status=status)
        return await self.select_models_order(db, 'sort', **filters)

    async def get_role_menus(self, db: AsyncSession, superuser: bool, menu_ids: list[int]) -> Sequence[Menu]:
        """
        Get Role Menu List

        :param db: database session
        :param superuser: is there a superadministrator
        :param menu_ids: menu ID list
        :return:
        """
        stmt = select(self.model).order_by(asc(self.model.sort))
        filters = [self.model.type.in_([0, 1])]
        if not superuser:
            filters.append(self.model.id.in_(menu_ids))
        stmt = stmt.where(and_(*filters))
        menu = await db.execute(stmt)
        return menu.scalars().all()

    async def create(self, db: AsyncSession, obj: CreateMenuParam) -> None:
        """
        Create Menu

        :param db: database session
        :param obj: create menu parameters
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, menu_id: int, obj: UpdateMenuParam) -> int:
        """
        Update Menu

        :param db: database session
        :param menu_id: menu ID
        :param obj: update menu parameters
        :return:
        """
        return await self.update_model(db, menu_id, obj)

    async def delete(self, db: AsyncSession, menu_id: int) -> int:
        """
        Remove Menu

        :param db: database session
        :param menu_id: menu ID
        :return:
        """
        return await self.delete_model(db, menu_id)

    async def get_children(self, db: AsyncSession, menu_id: int) -> list[Menu | None]:
        """
        Fetch Submenu List

        :param db: database session
        :param menu_id: menu ID
        :return:
        """
        stmt = select(self.model).options(selectinload(self.model.children)).where(self.model.id == menu_id)
        result = await db.execute(stmt)
        menu = result.scalars().first()
        return menu.children


menu_dao: CRUDMenu = CRUDMenu(Menu)
