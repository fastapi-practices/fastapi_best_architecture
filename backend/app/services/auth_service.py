#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from fastapi import Request
from fastapi.security import OAuth2PasswordRequestForm
from starlette.background import BackgroundTask, BackgroundTasks

from backend.app.common import jwt
from backend.app.common.enums import LoginLogStatusType
from backend.app.common.exception import errors
from backend.app.common.jwt import get_token
from backend.app.common.redis import redis_client
from backend.app.common.response.response_code import CustomErrorCode
from backend.app.core.conf import settings
from backend.app.crud.crud_user import UserDao
from backend.app.database.db_mysql import async_db_session
from backend.app.models import User
from backend.app.schemas.user import AuthLogin
from backend.app.services.login_log_service import LoginLogService
from backend.app.utils.timezone import timezone


class AuthService:
    login_time = timezone.now()

    async def swagger_login(self, *, form_data: OAuth2PasswordRequestForm) -> tuple[str, User]:
        async with async_db_session() as db:
            current_user = await UserDao.get_by_username(db, form_data.username)
            if not current_user:
                raise errors.NotFoundError(msg='用户不存在')
            elif not await jwt.password_verify(form_data.password + current_user.salt, current_user.password):
                raise errors.AuthorizationError(msg='密码错误')
            elif not current_user.status:
                raise errors.AuthorizationError(msg='用户已锁定, 登陆失败')
            # 更新登陆时间
            await UserDao.update_login_time(db, form_data.username, self.login_time)
            # 获取最新用户信息
            user = await UserDao.get(db, current_user.id)
            # 创建token
            access_token, _ = await jwt.create_access_token(str(user.id), multi_login=user.is_multi_login)
            return access_token, user

    async def login(
        self, *, request: Request, obj: AuthLogin, background_tasks: BackgroundTasks
    ) -> tuple[str, str, datetime, datetime, User]:
        async with async_db_session() as db:
            try:
                current_user = await UserDao.get_by_username(db, obj.username)
                if not current_user:
                    raise errors.NotFoundError(msg='用户不存在')
                elif not await jwt.password_verify(obj.password + current_user.salt, current_user.password):
                    raise errors.AuthorizationError(msg='密码错误')
                elif not current_user.status:
                    raise errors.AuthorizationError(msg='用户已锁定, 登陆失败')
                captcha_code = await redis_client.get(f'{settings.CAPTCHA_LOGIN_REDIS_PREFIX}:{request.state.ip}')
                if not captcha_code:
                    raise errors.AuthorizationError(msg='验证码失效，请重新获取')
                if captcha_code.lower() != obj.captcha.lower():
                    raise errors.CustomError(error=CustomErrorCode.CAPTCHA_ERROR)
                await UserDao.update_login_time(db, obj.username, self.login_time)
                user = await UserDao.get(db, current_user.id)
                access_token, access_token_expire_time = await jwt.create_access_token(
                    str(user.id), multi_login=user.is_multi_login
                )
                refresh_token, refresh_token_expire_time = await jwt.create_refresh_token(
                    str(user.id), access_token_expire_time, multi_login=user.is_multi_login
                )
            except errors.NotFoundError as e:
                raise errors.NotFoundError(msg=e.msg)
            except (errors.AuthorizationError, errors.CustomError) as e:
                err_log_info = dict(
                    db=db,
                    request=request,
                    user=current_user,
                    login_time=self.login_time,
                    status=LoginLogStatusType.fail.value,
                    msg=e.msg,
                )
                task = BackgroundTask(LoginLogService.create, **err_log_info)
                raise errors.AuthorizationError(msg=e.msg, background=task)
            except Exception as e:
                raise e
            else:
                log_info = dict(
                    db=db,
                    request=request,
                    user=user,
                    login_time=self.login_time,
                    status=LoginLogStatusType.success.value,
                    msg='登录成功',
                )
                background_tasks.add_task(LoginLogService.create, **log_info)
                await redis_client.delete(f'{settings.CAPTCHA_LOGIN_REDIS_PREFIX}:{request.state.ip}')
                return access_token, refresh_token, access_token_expire_time, refresh_token_expire_time, user

    @staticmethod
    async def new_token(*, request: Request, refresh_token: str) -> tuple[str, str, datetime, datetime]:
        user_id = await jwt.jwt_decode(refresh_token)
        if request.user.id != user_id:
            raise errors.TokenError(msg='刷新 token 无效')
        async with async_db_session() as db:
            current_user = await UserDao.get(db, user_id)
            if not current_user:
                raise errors.NotFoundError(msg='用户不存在')
            elif not current_user.status:
                raise errors.AuthorizationError(msg='用户已锁定，操作失败')
            current_token = await get_token(request)
            (
                new_access_token,
                new_refresh_token,
                new_access_token_expire_time,
                new_refresh_token_expire_time,
            ) = await jwt.create_new_token(
                str(current_user.id), current_token, refresh_token, multi_login=current_user.is_multi_login
            )
            return new_access_token, new_refresh_token, new_access_token_expire_time, new_refresh_token_expire_time

    @staticmethod
    async def logout(*, request: Request) -> None:
        token = await get_token(request)
        if request.user.is_multi_login:
            key = f'{settings.TOKEN_REDIS_PREFIX}:{request.user.id}:{token}'
            await redis_client.delete(key)
        else:
            prefix = f'{settings.TOKEN_REDIS_PREFIX}:{request.user.id}:'
            await redis_client.delete_prefix(prefix)
