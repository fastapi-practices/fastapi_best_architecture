from datetime import datetime

from fastapi import Request
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.admin.crud.crud_login_log import login_log_dao
from backend.app.admin.schema.login_log import CreateLoginLogParam, DeleteLoginLogParam
from backend.common.context import ctx
from backend.common.log import log


class LoginLogService:
    """登录日志服务类"""

    @staticmethod
    async def get_select(*, username: str | None, status: int | None, ip: str | None) -> Select:
        """
        获取登录日志列表查询条件

        :param username: 用户名
        :param status: 状态
        :param ip: IP 地址
        :return:
        """
        return await login_log_dao.get_list(username=username, status=status, ip=ip)

    @staticmethod
    async def create(
        *,
        db: AsyncSession,
        request: Request,
        user_uuid: str,
        username: str,
        login_time: datetime,
        status: int,
        msg: str,
    ) -> None:
        """
        创建登录日志

        :param db: 数据库会话
        :param request: FastAPI 请求对象
        :param user_uuid: 用户 UUID
        :param username: 用户名
        :param login_time: 登录时间
        :param status: 状态
        :param msg: 消息
        :return:
        """
        try:
            obj = CreateLoginLogParam(
                user_uuid=user_uuid,
                username=username,
                status=status,
                ip=ctx.ip,
                country=ctx.country,
                region=ctx.region,
                city=ctx.city,
                user_agent=ctx.user_agent,
                browser=ctx.browser,
                os=ctx.os,
                device=ctx.device,
                msg=msg,
                login_time=login_time,
            )
            await login_log_dao.create(db, obj)
        except Exception as e:
            log.error(f'登录日志创建失败: {e}')

    @staticmethod
    async def delete(*, db: AsyncSession, obj: DeleteLoginLogParam) -> int:
        """
        批量删除登录日志

        :param db: 数据库会话
        :param obj: 日志 ID 列表
        :return:
        """
        count = await login_log_dao.delete(db, obj.pks)
        return count

    @staticmethod
    async def delete_all(*, db: AsyncSession) -> None:
        """清空所有登录日志"""
        await login_log_dao.delete_all(db)


login_log_service: LoginLogService = LoginLogService()
