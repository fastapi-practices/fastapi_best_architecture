#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.plugin.notice.model import Notice
from backend.plugin.notice.schema.notice import CreateNoticeParam, UpdateNoticeParam


class CRUDNotice(CRUDPlus[Notice]):
    """Notify bulletin database operating class"""

    async def get(self, db: AsyncSession, pk: int) -> Notice | None:
        """
        Access to notice announcements

        :param db: database session
        :param pk: Notification bulletin ID
        :return:
        """
        return await self.select_model(db, pk)

    async def get_list(self) -> Select:
        """Get Notification Bulletin List"""
        return await self.select_order('created_time', 'desc')

    async def get_all(self, db: AsyncSession) -> Sequence[Notice]:
        """
        Get all notices posted

        :param db: database session
        :return:
        """
        return await self.select_models(db)

    async def create(self, db: AsyncSession, obj: CreateNoticeParam) -> None:
        """
        Create Notification Bulletin

        :param db: database session
        :param obj: create notification bulletin parameters
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateNoticeParam) -> int:
        """
        Update notification bulletins

        :param db: database session
        :param pk: Notification bulletin ID
        :param obj: update announcement parameters
        :return:
        """
        return await self.update_model(db, pk, obj)

    async def delete(self, db: AsyncSession, pk: list[int]) -> int:
        """
        Delete Notification Bulletin

        :param db: database session
        :param pk: Notification Bulletin ID list
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pk)


notice_dao: CRUDNotice = CRUDNotice(Notice)
