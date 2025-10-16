from typing import Any

from fast_captcha import text_captcha
from fastapi import BackgroundTasks, Response
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.admin.crud.crud_user import user_dao
from backend.app.admin.schema.token import GetLoginToken
from backend.app.admin.schema.user import AddOAuth2UserParam
from backend.app.admin.service.login_log_service import login_log_service
from backend.common.context import ctx
from backend.common.enums import LoginLogStatusType, UserSocialType
from backend.common.i18n import t
from backend.common.security import jwt
from backend.core.conf import settings
from backend.database.redis import redis_client
from backend.plugin.oauth2.crud.crud_user_social import user_social_dao
from backend.plugin.oauth2.schema.user_social import CreateUserSocialParam
from backend.utils.timezone import timezone


class OAuth2Service:
    """OAuth2 认证服务类"""

    @staticmethod
    async def create_with_login(
        *,
        db: AsyncSession,
        response: Response,
        background_tasks: BackgroundTasks,
        user: dict[str, Any],
        social: UserSocialType,
    ) -> GetLoginToken | None:
        """
        创建 OAuth2 用户并登录

        :param db: 数据库会话
        :param response: FastAPI 响应对象
        :param background_tasks: FastAPI 后台任务
        :param user: OAuth2 用户信息
        :param social: 社交平台类型
        :return:
        """

        sid = user.get('uuid')
        username = user.get('username')
        nickname = user.get('nickname')
        email = user.get('email')
        avatar = user.get('avatar_url')

        if social == UserSocialType.github:
            sid = user.get('id')
            username = user.get('login')
            nickname = user.get('name')

        if social == UserSocialType.google:
            sid = user.get('id')
            username = user.get('name')
            nickname = user.get('given_name')
            avatar = user.get('picture')

        if social == UserSocialType.linux_do:
            sid = user.get('id')
            nickname = user.get('name')

        user_social = await user_social_dao.get_by_sid(db, str(sid), str(social.value))
        if user_social:
            sys_user = await user_dao.get(db, user_social.user_id)
            # 更新用户头像
            if not sys_user.avatar and avatar is not None:
                await user_dao.update_avatar(db, sys_user.id, avatar)
        else:
            sys_user = None
            # 检测系统用户是否已存在
            if email:
                sys_user = await user_dao.check_email(db, email)  # 通过邮箱验证绑定保证邮箱真实性

            # 创建系统用户
            if not sys_user:
                while await user_dao.get_by_username(db, username):
                    username = f'{username}_{text_captcha(5)}'
                new_sys_user = AddOAuth2UserParam(
                    username=username,
                    password=None,
                    nickname=nickname,
                    email=email,
                    avatar=avatar,
                )
                await user_dao.add_by_oauth2(db, new_sys_user)
                await db.flush()
                sys_user = await user_dao.get_by_username(db, username)

            # 绑定社交账号
            new_user_social = CreateUserSocialParam(sid=str(sid), source=social.value, user_id=sys_user.id)
            await user_social_dao.create(db, new_user_social)

        # 创建 token
        access_token = await jwt.create_access_token(
            sys_user.id,
            multi_login=sys_user.is_multi_login,
            # extra info
            username=sys_user.username,
            nickname=sys_user.nickname or f'#{text_captcha(5)}',
            last_login_time=timezone.to_str(timezone.now()),
            ip=ctx.ip,
            os=ctx.os,
            browser=ctx.browser,
            device=ctx.device,
        )
        refresh_token = await jwt.create_refresh_token(
            access_token.session_uuid,
            sys_user.id,
            multi_login=sys_user.is_multi_login,
        )
        await user_dao.update_login_time(db, sys_user.username)
        await db.refresh(sys_user)
        background_tasks.add_task(
            login_log_service.create,
            db=db,
            user_uuid=sys_user.uuid,
            username=sys_user.username,
            login_time=timezone.now(),
            status=LoginLogStatusType.success.value,
            msg=t('success.login.oauth2_success'),
        )
        await redis_client.delete(f'{settings.CAPTCHA_LOGIN_REDIS_PREFIX}:{ctx.ip}')
        response.set_cookie(
            key=settings.COOKIE_REFRESH_TOKEN_KEY,
            value=refresh_token.refresh_token,
            max_age=settings.COOKIE_REFRESH_TOKEN_EXPIRE_SECONDS,
            expires=timezone.to_utc(refresh_token.refresh_token_expire_time),
            httponly=True,
        )
        data = GetLoginToken(
            access_token=access_token.access_token,
            access_token_expire_time=access_token.access_token_expire_time,
            session_uuid=access_token.session_uuid,
            user=sys_user,  # type: ignore
        )
        return data


oauth2_service: OAuth2Service = OAuth2Service()
