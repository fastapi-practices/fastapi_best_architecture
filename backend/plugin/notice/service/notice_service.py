#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select

from backend.common.exception import errors
from backend.database.db import async_db_session
from backend.plugin.notice.crud.crud_notice import notice_dao
from backend.plugin.notice.model import Notice
from backend.plugin.notice.schema.notice import CreateNoticeParam, UpdateNoticeParam


class NoticeService:
    """Notification service category"""

    @staticmethod
    async def get(*, pk: int) -> Notice:
        """
        Access to notice announcements

        :param pk: Notification bulletin ID
        :return:
        """
        async with async_db_session() as db:
            notice = await notice_dao.get(db, pk)
            if not notice:
                raise errors.NotFoundError(msg='Notifier announcement does not exist')
            return notice

    @staticmethod
    async def get_select() -> Select:
        """Get Notification Bulletin Queryer"""
        return await notice_dao.get_list()

    @staticmethod
    async def get_all() -> Sequence[Notice]:
        """Get all notices posted"""
        async with async_db_session() as db:
            notices = await notice_dao.get_all(db)
            return notices

    @staticmethod
    async def create(*, obj: CreateNoticeParam) -> None:
        """
        Create Notification Bulletin

        :param obj: create notification bulletin parameters
        :return:
        """
        async with async_db_session.begin() as db:
            await notice_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateNoticeParam) -> int:
        """
        Update notification bulletins

        :param pk: Notification bulletin ID
        :param obj: update announcement parameters
        :return:
        """
        async with async_db_session.begin() as db:
            notice = await notice_dao.get(db, pk)
            if not notice:
                raise errors.NotFoundError(msg='Notifier announcement does not exist')
            count = await notice_dao.update(db, pk, obj)
            return count

    @staticmethod
    async def delete(*, pk: list[int]) -> int:
        """
        Delete Notification Bulletin

        :param pk: Notification Bulletin ID list
        :return:
        """
        async with async_db_session.begin() as db:
            count = await notice_dao.delete(db, pk)
            return count


notice_service: NoticeService = NoticeService()
