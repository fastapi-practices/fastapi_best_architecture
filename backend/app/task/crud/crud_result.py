from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.task.model import TaskResult


class CRUDTaskResult(CRUDPlus[TaskResult]):
    """任务结果数据库操作类"""

    async def get(self, db: AsyncSession, pk: int) -> TaskResult | None:
        """
        获取任务结果详情

        :param db: 数据库会话
        :param pk: 任务 ID
        :return:
        """
        return await self.select_model(db, pk)

    async def get_select(self, name: str | None, task_id: str | None) -> Select:
        """
        获取任务结果列表查询表达式

        :param name: 任务名称
        :param task_id: 任务 ID
        :return:
        """
        filters = {}

        if name is not None:
            filters['name__like'] = f'%{name}%'
        if task_id is not None:
            filters['task_id'] = task_id

        return await self.select_order('id', 'desc', **filters)

    async def delete(self, db: AsyncSession, pks: list[int]) -> int:
        """
        批量删除任务结果

        :param db: 数据库会话
        :param pks: 任务结果 ID 列表
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pks)


task_result_dao: CRUDTaskResult = CRUDTaskResult(TaskResult)
