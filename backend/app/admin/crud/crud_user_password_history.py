from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model.user_password_history import UserPasswordHistory
from backend.app.admin.schema.user_password_history import CreateUserPasswordHistoryParam


class CRUDUserPasswordHistory(CRUDPlus[UserPasswordHistory]):
    """用户密码历史记录数据库操作类"""

    async def create(self, db: AsyncSession, obj: CreateUserPasswordHistoryParam) -> None:
        """
        创建密码历史记录

        :param db: 数据库会话
        :param obj: 创建密码历史记录参数
        :return:
        """
        await self.create_model(db, obj)

    async def get_by_user_id(self, db: AsyncSession, user_id: int) -> Sequence[UserPasswordHistory]:
        """
        获取用户的密码历史记录

        :param db: 数据库会话
        :param user_id: 用户 ID
        :return:
        """
        return await self.select_models_order(db, 'id', 'desc', self.model.user_id == user_id)


user_password_history_dao: CRUDUserPasswordHistory = CRUDUserPasswordHistory(UserPasswordHistory)
