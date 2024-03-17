#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.admin.model.sys_user_social import UserSocial
from backend.app.admin.schema.user_social import CreateUserSocialParam, UpdateUserSocialParam
from backend.common.enums import UserSocialType
from backend.common.msd.crud import CRUDBase


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
