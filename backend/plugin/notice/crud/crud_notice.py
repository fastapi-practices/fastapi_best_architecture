#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.plugin.notice.model import Notice
from backend.plugin.notice.schema.notice import CreateNoticeParam, UpdateNoticeParam


class CRUDNotice(CRUDPlus[Notice]):
    async def get(self, db: AsyncSession, pk: int) -> Notice | None:
        """
        获取系统通知公告

        :param db:
        :param pk:
        :return:
        """
        return await self.select_model(db, pk)

    async def get_list(self) -> Select:
        """
        获取系统通知公告列表

        :return:
        """
        return await self.select_order('created_time', 'desc')

    async def get_all(self, db: AsyncSession) -> Sequence[Notice]:
        """
        获取所有系统通知公告

        :param db:
        :return:
        """
        return await self.select_models(db)

    async def create(self, db: AsyncSession, obj_in: CreateNoticeParam) -> None:
        """
        创建系统通知公告

        :param db:
        :param obj_in:
        :return:
        """
        await self.create_model(db, obj_in)

    async def update(self, db: AsyncSession, pk: int, obj_in: UpdateNoticeParam) -> int:
        """
        更新系统通知公告

        :param db:
        :param pk:
        :param obj_in:
        :return:
        """
        return await self.update_model(db, pk, obj_in)

    async def delete(self, db: AsyncSession, pk: list[int]) -> int:
        """
        删除系统通知公告

        :param db:
        :param pk:
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pk)


notice_dao: CRUDNotice = CRUDNotice(Notice)
