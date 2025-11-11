from sqlalchemy.ext.asyncio import AsyncSession

from backend.common.exception import errors
from backend.plugin.oauth2.crud.crud_user_social import user_social_dao
from backend.plugin.oauth2.enums import UserSocialType


class UserSocialService:
    @staticmethod
    async def unbinding(*, db: AsyncSession, user_id: int, source: UserSocialType) -> int:
        """
        解绑用户社交账号

        :param db: 数据库会话
        :param user_id: 用户 ID
        :param source: 解绑源
        :return:
        """
        bind = user_social_dao.check_binding(db, user_id, source.value)
        if not bind:
            raise errors.NotFoundError(msg=f'用户未绑定 {source.value} 账号')
        return await user_social_dao.delete(db, user_id, source.value)


user_social_service: UserSocialService = UserSocialService()
