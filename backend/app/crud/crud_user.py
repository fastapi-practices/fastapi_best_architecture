#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Optional, NoReturn

from sqlalchemy import func, select, update, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from backend.app.api import jwt
from backend.app.crud.base import CRUDBase
from backend.app.models import User
from backend.app.schemas.user import CreateUser, UpdateUser, Avatar


class CRUDUser(CRUDBase[User, CreateUser, UpdateUser]):
    async def get_user_by_id(self, db: AsyncSession, user_id: int) -> User | None:
        return await self.get(db, user_id)

    async def get_user_by_username(self, db: AsyncSession, username: str) -> User | None:
        user = await db.execute(select(self.model).where(self.model.username == username))
        return user.scalars().first()

    async def update_user_login_time(self, db: AsyncSession, username: str) -> int:
        user = await db.execute(update(self.model).where(self.model.username == username).values(last_login=func.now()))
        return user.rowcount

    async def create_user(self, db: AsyncSession, create: CreateUser) -> NoReturn:
        create.password = jwt.get_hash_password(create.password)
        new_user = self.model(**create.dict())
        db.add(new_user)

    async def update_userinfo(self, db: AsyncSession, current_user: User, obj: UpdateUser) -> int:
        user = await db.execute(update(self.model).where(self.model.id == current_user.id).values(**obj.dict()))
        return user.rowcount

    async def update_avatar(self, db: AsyncSession, current_user: User, avatar: Avatar) -> int:
        user = await db.execute(update(self.model).where(self.model.id == current_user.id).values(avatar=avatar))
        return user.rowcount

    async def delete_user(self, db: AsyncSession, user_id: int) -> int:
        return await self.delete(db, user_id)

    async def check_email(self, db: AsyncSession, email: str) -> User:
        mail = await db.execute(select(self.model).where(self.model.email == email))
        return mail.scalars().first()

    async def reset_password(self, db: AsyncSession, pk: int, password: str) -> int:
        user = await db.execute(
            update(self.model).where(self.model.id == pk).values(password=jwt.get_hash_password(password))
        )
        return user.rowcount

    def get_users(self) -> Select:
        return select(self.model).order_by(desc(self.model.time_joined))

    async def get_user_is_super(self, db: AsyncSession, user_id: int) -> bool:
        user = await self.get_user_by_id(db, user_id)
        return user.is_superuser

    async def get_user_is_active(self, db: AsyncSession, user_id: int) -> bool:
        user = await self.get_user_by_id(db, user_id)
        return user.is_active

    async def super_set(self, db: AsyncSession, user_id: int) -> int:
        super_status = await self.get_user_is_super(db, user_id)
        user = await db.execute(
            update(self.model).where(self.model.id == user_id).values(is_superuser=False if super_status else True)
        )
        return user.rowcount

    async def active_set(self, db: AsyncSession, user_id: int) -> int:
        active_status = await self.get_user_is_active(db, user_id)
        user = await db.execute(
            update(self.model).where(self.model.id == user_id).values(is_active=False if active_status else True)
        )
        return user.rowcount


UserDao: CRUDUser = CRUDUser(User)
