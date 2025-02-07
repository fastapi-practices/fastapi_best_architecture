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
    @staticmethod
    async def get(*, pk: int) -> Notice:
        async with async_db_session() as db:
            notice = await notice_dao.get(db, pk)
            if not notice:
                raise errors.NotFoundError(msg='通知公告不存在')
            return notice

    @staticmethod
    async def get_select() -> Select:
        return await notice_dao.get_list()

    @staticmethod
    async def get_all() -> Sequence[Notice]:
        async with async_db_session() as db:
            notices = await notice_dao.get_all(db)
            return notices

    @staticmethod
    async def create(*, obj: CreateNoticeParam) -> None:
        async with async_db_session.begin() as db:
            await notice_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateNoticeParam) -> int:
        async with async_db_session.begin() as db:
            notice = await notice_dao.get(db, pk)
            if not notice:
                raise errors.NotFoundError(msg='通知公告不存在')
            count = await notice_dao.update(db, pk, obj)
            return count

    @staticmethod
    async def delete(*, pk: list[int]) -> int:
        async with async_db_session.begin() as db:
            count = await notice_dao.delete(db, pk)
            return count


notice_service: NoticeService = NoticeService()
