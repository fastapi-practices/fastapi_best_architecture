#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select, and_, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import noload, selectinload
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import DataScope, Menu, Role, User
from backend.app.admin.schema.role import (
    CreateRoleParam,
    UpdateRoleMenuParam,
    UpdateRoleParam,
    UpdateRoleScopeParam,
)


class CRUDRole(CRUDPlus[Role]):
    """Role Database Operator Category"""

    async def get(self, db: AsyncSession, role_id: int) -> Role | None:
        """
        Get Role Details

        :param db: database session
        :param role id
        :return:
        """
        return await self.select_model(db, role_id)

    async def get_with_relation(self, db: AsyncSession, role_id: int) -> Role | None:
        """
        Access to role and association data

        :param db: database session
        :param role id
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
        Get All Roles

        :param db: database session
        :return:
        """
        return await self.select_models(db)

    async def get_users(self, db: AsyncSession, user_id: int) -> Sequence[Role]:
        """
        Get User Roles List

        :param db: database session
        :param user_id: userID
        :return:
        """
        stmt = select(self.model).join(self.model.users).where(User.id == user_id)
        roles = await db.execute(stmt)
        return roles.scalars().all()

    async def get_list(self, name: str | None, status: int | None) -> Select:
        """
        Get Role List

        :param name: role name
        :param role status:
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
        Get roles by name

        :param db: database session
        :param name: role name
        :return:
        """
        return await self.select_model_by_column(db, name=name)

    async def create(self, db: AsyncSession, obj: CreateRoleParam) -> None:
        """
        Create Role

        :param db: database session
        :param obj: create role parameters
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, role_id: int, obj: UpdateRoleParam) -> int:
        """
        Update Role

        :param db: database session
        :param role id
        :param obj: update role parameters
        :return:
        """
        return await self.update_model(db, role_id, obj)

    async def update_menus(self, db: AsyncSession, role_id: int, menu_ids: UpdateRoleMenuParam) -> int:
        """
        Update Role Menu

        :param db: database session
        :param role id
        :param menu_ids: menu ID list
        :return:
        """
        current_role = await self.get_with_relation(db, role_id)
        stmt = select(Menu).where(Menu.id.in_(menu_ids.menus))
        menus = await db.execute(stmt)
        current_role.menus = menus.scalars().all()
        return len(current_role.menus)

    async def update_scopes(self, db: AsyncSession, role_id: int, scope_ids: UpdateRoleScopeParam) -> int:
        """
        Update role data range

        :param db: database session
        :param role id
        :param scope_ids: Permission range ID list
        :return:
        """
        current_role = await self.get_with_relation(db, role_id)
        stmt = select(DataScope).where(DataScope.id.in_(scope_ids.scopes))
        scopes = await db.execute(stmt)
        current_role.scopes = scopes.scalars().all()
        return len(current_role.scopes)

    async def delete(self, db: AsyncSession, role_id: list[int]) -> int:
        """
        Remove Role

        :param db: database session
        :param rOLE_id: Role ID list
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=role_id)


role_dao: CRUDRole = CRUDRole(Role)
