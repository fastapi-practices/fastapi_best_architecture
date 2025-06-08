#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.plugin.oauth2.model import UserSocial
from backend.plugin.oauth2.schema.user_social import CreateUserSocialParam


class CRUDUserSocial(CRUDPlus[UserSocial]):
    """用户社交账号数据库操作类"""

    async def check_binding(self, db: AsyncSession, pk: int, source: str) -> UserSocial | None:
        """
        检查系统用户社交账号绑定

        :param db: 数据库会话
        :param pk: 用户 ID
        :param source: 社交账号类型
        :return:
        """
        return await self.select_model_by_column(db, user_id=pk, source=source)

    async def get_by_sid(self, db: AsyncSession, sid: str, source: str) -> UserSocial | None:
        """
        通过 UUID 获取社交用户

        :param db: 数据库会话
        :param sid: 第三方 UUID
        :param source: 社交账号类型
        :return:
        """
        return await self.select_model_by_column(db, sid=sid, source=source)

    async def create(self, db: AsyncSession, obj: CreateUserSocialParam) -> None:
        """
        创建用户社交账号绑定

        :param db: 数据库会话
        :param obj: 创建用户社交账号绑定参数
        :return:
        """
        await self.create_model(db, obj)

    async def delete(self, db: AsyncSession, social_id: int) -> int:
        """
        删除用户社交账号绑定

        :param db: 数据库会话
        :param social_id: 社交账号绑定 ID
        :return:
        """
        return await self.delete_model(db, social_id)


user_social_dao: CRUDUserSocial = CRUDUserSocial(UserSocial)
