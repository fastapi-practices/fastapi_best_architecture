#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import NoReturn

from fastapi import Request
from fastapi.security import OAuth2PasswordRequestForm
from pydantic.datetime_parse import parse_datetime
from starlette.background import BackgroundTasks, BackgroundTask

from backend.app.common import jwt
from backend.app.common.enums import LoginLogStatus
from backend.app.common.exception import errors
from backend.app.common.jwt import get_token
from backend.app.common.redis import redis_client
from backend.app.core.conf import settings
from backend.app.crud.crud_user import UserDao
from backend.app.database.db_mysql import async_db_session
from backend.app.schemas.user import Auth
from backend.app.services.login_log_service import LoginLogService


class AuthService:
    login_time = parse_datetime(datetime.now())

    async def swagger_login(self, form_data: OAuth2PasswordRequestForm):
        async with async_db_session() as db:
            current_user = await UserDao.get_by_username(db, form_data.username)
            if not current_user:
                raise errors.NotFoundError(msg='用户不存在')
            elif not jwt.password_verify(form_data.password, current_user.password):
                raise errors.AuthorizationError(msg='密码错误')
            elif not current_user.is_active:
                raise errors.AuthorizationError(msg='用户已锁定, 登陆失败')
            # 更新登陆时间
            await UserDao.update_login_time(db, form_data.username, self.login_time)
            # 查询用户角色
            user_role_ids = await UserDao.get_role_ids(db, current_user.id)
            # 获取最新用户信息
            user = await UserDao.get(db, current_user.id)
            # 创建token
            access_token, _ = await jwt.create_access_token(
                str(user.id), role_ids=user_role_ids, multi_login=user.is_multi_login
            )
            return access_token, user

    async def login(self, *, request: Request, obj: Auth, background_tasks: BackgroundTasks):
        async with async_db_session() as db:
            try:
                current_user = await UserDao.get_by_username(db, obj.username)
                if not current_user:
                    raise errors.NotFoundError(msg='用户不存在')
                elif not jwt.password_verify(obj.password, current_user.password):
                    raise errors.AuthorizationError(msg='密码错误')
                elif not current_user.is_active:
                    raise errors.AuthorizationError(msg='用户已锁定, 登陆失败')
                await UserDao.update_login_time(db, obj.username, self.login_time)
                user_role_ids = await UserDao.get_role_ids(db, current_user.id)
                user = await UserDao.get(db, current_user.id)
                access_token, access_token_expire_time = await jwt.create_access_token(
                    str(user.id), role_ids=user_role_ids, multi_login=user.is_multi_login
                )
                refresh_token, refresh_token_expire_time = await jwt.create_refresh_token(
                    str(user.id), access_token_expire_time, role_ids=user_role_ids, multi_login=user.is_multi_login
                )
            except errors.NotFoundError as e:
                raise errors.NotFoundError(msg=e.msg)
            except errors.AuthorizationError as e:
                err_log_info = dict(
                    db=db,
                    request=request,
                    user=current_user,
                    login_time=self.login_time,
                    status=LoginLogStatus.fail,
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
                    status=LoginLogStatus.success,
                    msg='登录成功',
                )
                background_tasks.add_task(LoginLogService.create, **log_info)
                return access_token, refresh_token, access_token_expire_time, refresh_token_expire_time, user

    @staticmethod
    async def new_token(refresh_token: str) -> tuple[str, datetime]:
        user_id, role_ids = jwt.jwt_decode(refresh_token)
        async with async_db_session() as db:
            current_user = await UserDao.get(db, user_id)
            if not current_user:
                raise errors.NotFoundError(msg='用户不存在')
            elif not current_user.is_active:
                raise errors.AuthorizationError(msg='用户已锁定, 获取失败')
            access_new_token, access_new_token_expire_time = await jwt.create_new_token(
                str(current_user.id), refresh_token, role_ids=role_ids, multi_login=current_user.is_multi_login
            )
            return access_new_token, access_new_token_expire_time

    @staticmethod
    async def logout(request: Request) -> NoReturn:
        token = get_token(request)
        if request.user.is_multi_login:
            key = f'{settings.TOKEN_REDIS_PREFIX}:{request.user.id}:{token}'
            await redis_client.delete(key)
        else:
            prefix = f'{settings.TOKEN_REDIS_PREFIX}:{request.user.id}:'
            await redis_client.delete_prefix(prefix)
