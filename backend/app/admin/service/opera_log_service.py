#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select

from backend.app.admin.crud.crud_opera_log import opera_log_dao
from backend.app.admin.schema.opera_log import CreateOperaLogParam, DeleteOperaLogParam
from backend.common.log import log
from backend.common.queue import get_many_from_queue, opera_log_queue
from backend.database.db import async_db_session


class OperaLogService:
    """操作日志服务类"""

    @staticmethod
    async def get_select(*, username: str | None, status: int | None, ip: str | None) -> Select:
        """
        获取操作日志列表查询条件

        :param username: 用户名
        :param status: 状态
        :param ip: IP 地址
        :return:
        """
        return await opera_log_dao.get_list(username=username, status=status, ip=ip)

    @staticmethod
    async def create(*, obj: CreateOperaLogParam) -> None:
        """
        创建操作日志（同步）

        :param obj: 操作日志创建参数
        :return:
        """
        async with async_db_session.begin() as db:
            await opera_log_dao.create(db, obj)

    @staticmethod
    async def create_in_queue(*, obj: CreateOperaLogParam) -> None:
        """
        创建操作日志（入队）

        :param obj: 操作日志创建参数
        :return:
        """
        await opera_log_queue.put(obj)

    @staticmethod
    async def batch_create_consumer() -> None:
        """
        批量创建操作日志消费者

        :return:
        """
        while True:
            try:
                logs = await get_many_from_queue(opera_log_queue, max_items=100, timeout=1)
                if logs:
                    log.info(f"处理日志: {len(logs)} 条.", )
                    async with async_db_session.begin() as db:
                        await opera_log_dao.batch_create(db, logs)
                else:
                    log.debug("无日志可处理")

            except Exception as e:
                log.error(f'批量创建操作日志失败: {e}')
            finally:
                # 防止队列阻塞
                if not opera_log_queue.empty():
                    opera_log_queue.task_done()

    @staticmethod
    async def delete(*, obj: DeleteOperaLogParam) -> int:
        """
        批量删除操作日志

        :param obj: 日志 ID 列表
        :return:
        """
        async with async_db_session.begin() as db:
            count = await opera_log_dao.delete(db, obj.pks)
            return count

    @staticmethod
    async def delete_all() -> None:
        """清空所有操作日志"""
        async with async_db_session.begin() as db:
            await opera_log_dao.delete_all(db)


opera_log_service: OperaLogService = OperaLogService()
