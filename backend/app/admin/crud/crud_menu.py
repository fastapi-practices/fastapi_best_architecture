#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import and_, asc, select
from sqlalchemy.orm import selectinload
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import Menu
from backend.app.admin.schema.menu import CreateMenuParam, UpdateMenuParam


class CRUDMenu(CRUDPlus[Menu]):
    async def get(self, db, menu_id: int) -> Menu | None:
        """
        获取菜单

        :param db:
        :param menu_id:
        :return:
        """
        return await self.select_model(db, menu_id)

    async def get_by_title(self, db, title: str) -> Menu | None:
        """
        通过 title 获取菜单

        :param db:
        :param title:
        :return:
        """
        return await self.select_model_by_column(db, title=title, menu_type__ne=2)

    async def get_all(self, db, title: str | None = None, status: int | None = None) -> Sequence[Menu]:
        """
        获取所有菜单

        :param db:
        :param title:
        :param status:
        :return:
        """
        filters = {}
        if title is not None:
            filters.update(title=f'%{title}%')
        if status is not None:
            filters.update(status=status)
        return await self.select_models_order(db, 'sort', **filters)

    async def get_role_menus(self, db, superuser: bool, menu_ids: list[int]) -> Sequence[Menu]:
        """
        获取角色菜单

        :param db:
        :param superuser:
        :param menu_ids:
        :return:
        """
        stmt = select(self.model).order_by(asc(self.model.sort))
        where_list = [self.model.menu_type.in_([0, 1])]
        if not superuser:
            where_list.append(self.model.id.in_(menu_ids))
        stmt = stmt.where(and_(*where_list))
        menu = await db.execute(stmt)
        return menu.scalars().all()

    async def create(self, db, obj_in: CreateMenuParam) -> None:
        """
        创建菜单

        :param db:
        :param obj_in:
        :return:
        """
        await self.create_model(db, obj_in)

    async def update(self, db, menu_id: int, obj_in: UpdateMenuParam) -> int:
        """
        更新菜单

        :param db:
        :param menu_id:
        :param obj_in:
        :return:
        """
        return await self.update_model(db, menu_id, obj_in)

    async def delete(self, db, menu_id: int) -> int:
        """
        删除菜单

        :param db:
        :param menu_id:
        :return:
        """
        return await self.delete_model(db, menu_id)

    async def get_children(self, db, menu_id: int) -> list[Menu]:
        """
        获取子菜单

        :param db:
        :param menu_id:
        :return:
        """
        stmt = select(self.model).options(selectinload(self.model.children)).where(self.model.id == menu_id)
        result = await db.execute(stmt)
        menu = result.scalars().first()
        return menu.children


menu_dao: CRUDMenu = CRUDMenu(Menu)
