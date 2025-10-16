from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.admin.crud.crud_opera_log import opera_log_dao
from backend.app.admin.schema.opera_log import CreateOperaLogParam, DeleteOperaLogParam
from backend.common.pagination import paging_data


class OperaLogService:
    """操作日志服务类"""

    @staticmethod
    async def get_list(*, db: AsyncSession, username: str | None, status: int | None, ip: str | None) -> dict[str, Any]:
        """
        获取操作日志列表

        :param db: 数据库会话
        :param username: 用户名
        :param status: 状态
        :param ip: IP 地址
        :return:
        """
        log_select = await opera_log_dao.get_select(username=username, status=status, ip=ip)
        return await paging_data(db, log_select)

    @staticmethod
    async def create(*, db: AsyncSession, obj: CreateOperaLogParam) -> None:
        """
        创建操作日志

        :param db: 数据库会话
        :param obj: 操作日志创建参数
        :return:
        """
        await opera_log_dao.create(db, obj)

    @staticmethod
    async def bulk_create(*, db: AsyncSession, objs: list[CreateOperaLogParam]) -> None:
        """
        批量创建操作日志

        :param db: 数据库会话
        :param objs: 操作日志创建参数列表
        :return:
        """
        await opera_log_dao.bulk_create(db, objs)

    @staticmethod
    async def delete(*, db: AsyncSession, obj: DeleteOperaLogParam) -> int:
        """
        批量删除操作日志

        :param db: 数据库会话
        :param obj: 日志 ID 列表
        :return:
        """
        count = await opera_log_dao.delete(db, obj.pks)
        return count

    @staticmethod
    async def delete_all(*, db: AsyncSession) -> None:
        """
        清空所有操作日志

        :param db: 数据库会话
        :return:
        """
        await opera_log_dao.delete_all(db)


opera_log_service: OperaLogService = OperaLogService()
