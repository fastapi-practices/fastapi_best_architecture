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
    """菜单数据库操作类"""

    async def get(self, db: AsyncSession, menu_id: int) -> Menu | None:
        """
        获取菜单详情

        :param db: 数据库会话
        :param menu_id: 菜单 ID
        :return:
        """
        return await self.select_model(db, menu_id)

    async def get_by_title(self, db: AsyncSession, title: str) -> Menu | None:
        """
        通过标题获取菜单

        :param db: 数据库会话
        :param title: 菜单标题
        :return:
        """
        return await self.select_model_by_column(db, title=title, type__ne=2)

    async def get_all(self, db: AsyncSession, title: str | None, status: int | None) -> Sequence[Menu]:
        """
        获取菜单列表

        :param db: 数据库会话
        :param title: 菜单标题
        :param status: 菜单状态
        :return:
        """
        filters = {}
        if title is not None:
            filters.update(title__like=f'%{title}%')
        if status is not None:
            filters.update(status=status)
        return await self.select_models_order(db, 'sort', **filters)

    async def get_sidebar(self, db: AsyncSession, superuser: bool, menu_ids: list[int | None]) -> Sequence[Menu]:
        """
        获取角色菜单列表

        :param db: 数据库会话
        :param superuser: 是否超级管理员
        :param menu_ids: 菜单 ID 列表
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
        创建菜单

        :param db: 数据库会话
        :param obj: 创建菜单参数
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, menu_id: int, obj: UpdateMenuParam) -> int:
        """
        更新菜单

        :param db: 数据库会话
        :param menu_id: 菜单 ID
        :param obj: 更新菜单参数
        :return:
        """
        return await self.update_model(db, menu_id, obj)

    async def delete(self, db: AsyncSession, menu_id: int) -> int:
        """
        删除菜单

        :param db: 数据库会话
        :param menu_id: 菜单 ID
        :return:
        """
        return await self.delete_model(db, menu_id)

    async def get_children(self, db: AsyncSession, menu_id: int) -> list[Menu | None]:
        """
        获取子菜单列表

        :param db: 数据库会话
        :param menu_id: 菜单 ID
        :return:
        """
        stmt = select(self.model).options(selectinload(self.model.children)).where(self.model.id == menu_id)
        result = await db.execute(stmt)
        menu = result.scalars().first()
        return menu.children


menu_dao: CRUDMenu = CRUDMenu(Menu)
