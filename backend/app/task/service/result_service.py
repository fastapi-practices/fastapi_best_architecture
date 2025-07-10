#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import Select

from backend.app.task.crud.crud_result import task_result_dao
from backend.app.task.model.result import TaskResult
from backend.app.task.schema.result import DeleteTaskResultParam
from backend.common.exception import errors
from backend.database.db import async_db_session


class TaskResultService:
    @staticmethod
    async def get(*, pk: int) -> TaskResult:
        """
        获取任务结果详情

        :param pk: 任务 ID
        :return:
        """
        async with async_db_session() as db:
            result = await task_result_dao.get(db, pk)
            if not result:
                raise errors.NotFoundError(msg='任务结果不存在')
            return result

    @staticmethod
    async def get_select(*, name: str | None, task_id: str | None) -> Select:
        """
        获取任务结果列表查询条件

        :param name: 任务名称
        :param task_id: 任务 ID
        :return:
        """
        return await task_result_dao.get_list(name, task_id)

    @staticmethod
    async def delete(*, obj: DeleteTaskResultParam) -> int:
        """
        批量删除任务结果

        :param obj: 任务结果 ID 列表
        :return:
        """
        async with async_db_session.begin() as db:
            count = await task_result_dao.delete(db, obj.pks)
            return count


task_result_service: TaskResultService = TaskResultService()
