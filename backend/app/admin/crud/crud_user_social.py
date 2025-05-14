#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import UserSocial
from backend.app.admin.schema.user_social import CreateUserSocialParam
from backend.common.enums import UserSocialType


class CRUDUserSocial(CRUDPlus[UserSocial]):
    """User Social Account Database Operating Category"""

    async def get(self, db: AsyncSession, pk: int, source: UserSocialType) -> UserSocial | None:
        """
        Fetch user social account binding details

        :param db: database session
        :param pk: User ID
        :param source: social account type
        :return:
        """
        return await self.select_model_by_column(db, user_id=pk, source=source)

    async def create(self, db: AsyncSession, obj: CreateUserSocialParam) -> None:
        """
        Create user social account binding

        :param db: database session
        :param obj: create user social account binding parameters
        :return:
        """
        await self.create_model(db, obj)

    async def delete(self, db: AsyncSession, social_id: int) -> int:
        """
        Remove user social account binding

        :param db: database session
        :param social_id: social account binding ID
        :return:
        """
        return await self.delete_model(db, social_id)


user_social_dao: CRUDUserSocial = CRUDUserSocial(UserSocial)
