#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.app.common.exception import errors
from backend.app.crud.crud_menu import MenuDao
from backend.app.database.db_mysql import async_db_session
from backend.app.schemas.menu import CreateMenu, UpdateMenu
from backend.app.utils.build_tree import get_tree_data


class MenuService:
    @staticmethod
    async def get(pk: int):
        async with async_db_session() as db:
            menu = await MenuDao.get(db, menu_id=pk)
            return menu

    @staticmethod
    async def get_select(name: str | None = None, status: bool | None = None):
        async with async_db_session() as db:
            menu_select = await MenuDao.get_all(db, name=name, status=status)
            menu_tree = await get_tree_data(menu_select)
            return menu_tree

    @staticmethod
    async def create(obj: CreateMenu, user_id: int):
        async with async_db_session.begin() as db:
            menu = await MenuDao.get_by_name(db, obj.name)
            if menu:
                raise errors.ForbiddenError(msg='菜单名称已存在')
            new_obj = obj.dict()
            new_obj.update({'level': obj.parent_id + 1 if obj.parent_id else 1, 'create_user': user_id})
            await MenuDao.create(db, new_obj)

    @staticmethod
    async def update(pk: int, obj: UpdateMenu, user_id: int):
        async with async_db_session.begin() as db:
            menu = await MenuDao.get(db, pk)
            if not menu:
                raise errors.NotFoundError(msg='菜单不存在')
            if menu.name != obj.name:
                if await MenuDao.get_by_name(db, obj.name):
                    raise errors.ForbiddenError(msg='菜单名称已存在')
            new_obj = obj.dict()
            new_obj.update({'level': obj.parent_id + 1 if obj.parent_id else 1, 'update_user': user_id})
            count = await MenuDao.update(db, pk, new_obj)
            return count

    @staticmethod
    async def delete(pk: int):
        async with async_db_session.begin() as db:
            children = await MenuDao.get_children(db, pk)
            if children:
                raise errors.ForbiddenError(msg='菜单下存在子菜单，无法删除')
            count = await MenuDao.delete(db, pk)
            return count
