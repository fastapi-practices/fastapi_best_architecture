#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import UserSocial
from app.schemas.user_social import CreateUserSocialParam, UpdateUserSocialParam


class CRUDOUserSocial(CRUDBase[UserSocial, CreateUserSocialParam, UpdateUserSocialParam]):
    async def create(self, db: AsyncSession, obj_in: CreateUserSocialParam) -> None:
        await self.create_(db, obj_in)

    async def delete(self, db: AsyncSession, social_id: int) -> int:
        return await self.delete_(db, social_id)


user_social_dao: CRUDOUserSocial = CRUDOUserSocial(UserSocial)
