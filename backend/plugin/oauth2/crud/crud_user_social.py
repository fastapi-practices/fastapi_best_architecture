from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus, JoinConfig

from backend.app.admin.model import User
from backend.plugin.oauth2.model import UserSocial
from backend.plugin.oauth2.schema.user_social import CreateUserSocialParam


class CRUDUserSocial(CRUDPlus[UserSocial]):
    """用户社交账号数据库操作类"""

    async def check_binding(self, db: AsyncSession, user_id: int, source: str) -> UserSocial | None:
        """
        检查系统用户社交账号绑定

        :param db: 数据库会话
        :param user_id: 用户 ID
        :param source: 社交账号类型
        :return:
        """
        return await self.select_model_by_column(db, user_id=user_id, source=source)

    async def get_by_sid(
        self,
        db: AsyncSession,
        tenant_id: int,
        sid: str,
        source: str,
    ) -> UserSocial | None:
        """
        通过 sid 获取当前租户内的社交用户

        :param db: 数据库会话
        :param tenant_id: 租户 ID
        :param sid: 社交账号唯一编码
        :param source: 社交账号类型
        :return:
        """
        return await self.select_model_by_column(
            db,
            User.tenant_id == tenant_id,
            sid=sid,
            source=source,
            join_conditions=[JoinConfig(model=User, join_on=User.id == self.model.user_id)],
        )

    async def get_by_user_id(self, db: AsyncSession, user_id: int) -> Sequence[UserSocial]:
        """
        通过用户 ID 获取所有社交账号绑定

        :param db: 数据库会话
        :param user_id: 用户 ID
        :return:
        """
        return await self.select_models(db, user_id=user_id)

    async def create(self, db: AsyncSession, obj: CreateUserSocialParam) -> None:
        """
        创建用户社交账号绑定

        :param db: 数据库会话
        :param obj: 创建用户社交账号绑定参数
        :return:
        """
        await self.create_model(db, obj)

    async def delete(self, db: AsyncSession, user_id: int, source: str) -> int:
        """
        删除用户社交账号绑定

        :param db: 数据库会话
        :param user_id: 用户 ID
        :param source: 社交账号类型
        :return:
        """
        return await self.delete_model_by_column(db, user_id=user_id, source=source)

    async def delete_by_user_id(self, db: AsyncSession, user_id: int) -> int:
        """
        通过用户 ID 删除用户社交

        :param db: 数据库会话
        :param user_id: 用户 ID
        :return:
        """
        return await self.delete_model_by_column(db, user_id=user_id)


user_social_dao: CRUDUserSocial = CRUDUserSocial(UserSocial)
