#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select, and_, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import noload, selectinload
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import DataScope, Menu, Role
from backend.app.admin.schema.role import (
    CreateRoleParam,
    UpdateRoleMenuParam,
    UpdateRoleParam,
    UpdateRoleScopeParam,
)


class CRUDRole(CRUDPlus[Role]):
    """角色数据库操作类"""

    async def get(self, db: AsyncSession, role_id: int) -> Role | None:
        """
        获取角色详情

        :param db: 数据库会话
        :param role_id: 角色 ID
        :return:
        """
        return await self.select_model(db, role_id)

    async def get_with_relation(self, db: AsyncSession, role_id: int) -> Role | None:
        """
        获取角色及关联数据

        :param db: 数据库会话
        :param role_id: 角色 ID
        :return:
        """
        stmt = (
            select(self.model)
            .options(selectinload(self.model.menus), selectinload(self.model.scopes))
            .where(self.model.id == role_id)
        )
        role = await db.execute(stmt)
        return role.scalars().first()

    async def get_all(self, db: AsyncSession) -> Sequence[Role]:
        """
        获取所有角色

        :param db: 数据库会话
        :return:
        """
        return await self.select_models(db)

    async def get_list(self, name: str | None, status: int | None) -> Select:
        """
        获取角色列表

        :param name: 角色名称
        :param status: 角色状态
        :return:
        """
        stmt = (
            select(self.model)
            .options(noload(self.model.users), noload(self.model.menus), noload(self.model.scopes))
            .order_by(desc(self.model.created_time))
        )

        filters = []
        if name is not None:
            filters.append(self.model.name.like(f'%{name}%'))
        if status is not None:
            filters.append(self.model.status == status)

        if filters:
            stmt = stmt.where(and_(*filters))

        return stmt

    async def get_by_name(self, db: AsyncSession, name: str) -> Role | None:
        """
        通过名称获取角色

        :param db: 数据库会话
        :param name: 角色名称
        :return:
        """
        return await self.select_model_by_column(db, name=name)

    async def create(self, db: AsyncSession, obj: CreateRoleParam) -> None:
        """
        创建角色

        :param db: 数据库会话
        :param obj: 创建角色参数
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, role_id: int, obj: UpdateRoleParam) -> int:
        """
        更新角色

        :param db: 数据库会话
        :param role_id: 角色 ID
        :param obj: 更新角色参数
        :return:
        """
        return await self.update_model(db, role_id, obj)

    async def update_menus(self, db: AsyncSession, role_id: int, menu_ids: UpdateRoleMenuParam) -> int:
        """
        更新角色菜单

        :param db: 数据库会话
        :param role_id: 角色 ID
        :param menu_ids: 菜单 ID 列表
        :return:
        """
        current_role = await self.get_with_relation(db, role_id)
        stmt = select(Menu).where(Menu.id.in_(menu_ids.menus))
        menus = await db.execute(stmt)
        current_role.menus = menus.scalars().all()
        return len(current_role.menus)

    async def update_scopes(self, db: AsyncSession, role_id: int, scope_ids: UpdateRoleScopeParam) -> int:
        """
        更新角色数据范围

        :param db: 数据库会话
        :param role_id: 角色 ID
        :param scope_ids: 权限范围 ID 列表
        :return:
        """
        current_role = await self.get_with_relation(db, role_id)
        stmt = select(DataScope).where(DataScope.id.in_(scope_ids.scopes))
        scopes = await db.execute(stmt)
        current_role.scopes = scopes.scalars().all()
        return len(current_role.scopes)

    async def delete(self, db: AsyncSession, role_id: list[int]) -> int:
        """
        删除角色

        :param db: 数据库会话
        :param role_id: 角色 ID 列表
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=role_id)


role_dao: CRUDRole = CRUDRole(Role)
