#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.common.enums import UserSocialType
from backend.app.crud.base import CRUDBase
from backend.app.models import UserSocial
from backend.app.schemas.user_social import CreateUserSocialParam, UpdateUserSocialParam


class CRUDOUserSocial(CRUDBase[UserSocial, CreateUserSocialParam, UpdateUserSocialParam]):
    async def get(self, db: AsyncSession, pk: int, source: UserSocialType) -> UserSocial | None:
        se = select(self.model).where(and_(self.model.id == pk, self.model.source == source))
        user_social = await db.execute(se)
        return user_social.scalars().first()

    async def create(self, db: AsyncSession, obj_in: CreateUserSocialParam) -> None:
        await self.create_(db, obj_in)

    async def delete(self, db: AsyncSession, social_id: int) -> int:
        return await self.delete_(db, social_id)


user_social_dao: CRUDOUserSocial = CRUDOUserSocial(UserSocial)
