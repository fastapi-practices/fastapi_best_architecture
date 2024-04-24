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
        return await self.select_model_by_id(db, menu_id)

    async def get_by_title(self, db, title: str) -> Menu | None:
        """
        通过 title 获取菜单

        :param db:
        :param title:
        :return:
        """
        result = await db.execute(select(self.model).where(and_(self.model.title == title, self.model.menu_type != 2)))
        return result.scalars().first()

    async def get_all(self, db, title: str | None = None, status: int | None = None) -> Sequence[Menu]:
        """
        获取所有菜单

        :param db:
        :param title:
        :param status:
        :return:
        """
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
        """
        获取角色菜单

        :param db:
        :param superuser:
        :param menu_ids:
        :return:
        """
        se = select(self.model).order_by(asc(self.model.sort))
        where_list = [self.model.menu_type.in_([0, 1])]
        if not superuser:
            where_list.append(self.model.id.in_(menu_ids))
        se = se.where(and_(*where_list))
        menu = await db.execute(se)
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
        count = await self.update_model(db, menu_id, obj_in)
        return count

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
        result = await db.execute(
            select(self.model).options(selectinload(self.model.children)).where(self.model.id == menu_id)
        )
        menu = result.scalars().first()
        return menu.children


menu_dao: CRUDMenu = CRUDMenu(Menu)
