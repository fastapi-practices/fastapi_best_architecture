#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import NoReturn

from sqlalchemy import select, update, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import Select

from backend.app.common import jwt
from backend.app.crud.base import CRUDBase
from backend.app.models import User, Role
from backend.app.schemas.user import CreateUser, UpdateUser, Avatar


class CRUDUser(CRUDBase[User, CreateUser, UpdateUser]):
    async def get(self, db: AsyncSession, user_id: int) -> User | None:
        return await self.get_(db, user_id)

    async def get_by_username(self, db: AsyncSession, username: str) -> User | None:
        user = await db.execute(select(self.model).where(self.model.username == username))
        return user.scalars().first()

    async def update_login_time(self, db: AsyncSession, username: str, login_time: datetime) -> int:
        user = await db.execute(update(self.model).where(self.model.username == username).values(last_login=login_time))
        return user.rowcount

    async def create(self, db: AsyncSession, create: CreateUser) -> NoReturn:
        create.password = jwt.get_hash_password(create.password)
        new_user = self.model(**create.dict(exclude={'roles'}))
        role_list = []
        for role_id in create.roles:
            role_list.append(await db.get(Role, role_id))
        new_user.roles.append(*role_list)
        db.add(new_user)

    async def update_userinfo(self, db: AsyncSession, input_user: User, obj: UpdateUser) -> int:
        user = await db.execute(
            update(self.model).where(self.model.id == input_user.id).values(**obj.dict(exclude={'roles'}))
        )
        # 删除用户所有角色
        for i in list(input_user.roles):
            input_user.roles.remove(i)
        # 添加用户角色
        role_list = []
        for role_id in obj.roles:
            role_list.append(await db.get(Role, role_id))
        input_user.roles.append(*role_list)
        return user.rowcount

    async def update_avatar(self, db: AsyncSession, current_user: User, avatar: Avatar) -> int:
        user = await db.execute(update(self.model).where(self.model.id == current_user.id).values(avatar=avatar))
        return user.rowcount

    async def delete(self, db: AsyncSession, user_id: int) -> int:
        return await self.delete_(db, user_id)

    async def check_email(self, db: AsyncSession, email: str) -> User | None:
        mail = await db.execute(select(self.model).where(self.model.email == email))
        return mail.scalars().first()

    async def reset_password(self, db: AsyncSession, pk: int, password: str) -> int:
        user = await db.execute(
            update(self.model).where(self.model.id == pk).values(password=jwt.get_hash_password(password))
        )
        return user.rowcount

    def get_all(self) -> Select:
        return (
            select(self.model)
            .options(selectinload(self.model.roles).selectinload(Role.menus))
            .order_by(desc(self.model.time_joined))
        )

    async def get_super(self, db: AsyncSession, user_id: int) -> bool:
        user = await self.get(db, user_id)
        return user.is_superuser

    async def get_active(self, db: AsyncSession, user_id: int) -> bool:
        user = await self.get(db, user_id)
        return user.is_active

    async def set_super(self, db: AsyncSession, user_id: int) -> int:
        super_status = await self.get_super(db, user_id)
        user = await db.execute(
            update(self.model).where(self.model.id == user_id).values(is_superuser=False if super_status else True)
        )
        return user.rowcount

    async def set_active(self, db: AsyncSession, user_id: int) -> int:
        active_status = await self.get_active(db, user_id)
        user = await db.execute(
            update(self.model).where(self.model.id == user_id).values(is_active=False if active_status else True)
        )
        return user.rowcount

    async def get_role_ids(self, db: AsyncSession, user_id: int) -> list[int]:
        user = await db.execute(
            select(self.model).where(self.model.id == user_id).options(selectinload(self.model.roles))
        )
        roles_id = [role.id for role in user.scalars().first().roles]
        return roles_id

    async def get_with_relation(self, db: AsyncSession, *, user_id: int = None, username: str = None) -> User | None:
        where = []
        if user_id:
            where.append(self.model.id == user_id)
        if username:
            where.append(self.model.username == username)
        user = await db.execute(
            select(self.model)
            .options(selectinload(self.model.dept))
            .options(selectinload(self.model.roles).joinedload(Role.menus))
            .where(*where)
        )
        return user.scalars().first()


UserDao: CRUDUser = CRUDUser(User)
