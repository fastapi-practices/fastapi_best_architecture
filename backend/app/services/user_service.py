#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import NoReturn

from email_validator import validate_email, EmailNotValidError
from fastapi import Request
from fastapi.security import OAuth2PasswordRequestForm
from pydantic.datetime_parse import parse_datetime
from sqlalchemy import Select
from starlette.background import BackgroundTasks

from backend.app.common import jwt
from backend.app.common.exception import errors
from backend.app.common.redis import redis_client
from backend.app.core.conf import settings
from backend.app.crud.crud_dept import DeptDao
from backend.app.crud.crud_role import RoleDao
from backend.app.crud.crud_user import UserDao
from backend.app.database.db_mysql import async_db_session
from backend.app.models import User
from backend.app.schemas.token import RefreshTokenTime
from backend.app.schemas.user import CreateUser, ResetPassword, UpdateUser, Avatar, Auth
from backend.app.services.login_log_service import LoginLogService
from backend.app.utils import re_verify


class UserService:
    login_time = parse_datetime(datetime.utcnow())

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
            access_token, _ = await jwt.create_access_token(str(user.id), role_ids=user_role_ids)
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
                    str(user.id), role_ids=user_role_ids
                )
                refresh_token, refresh_token_expire_time = await jwt.create_refresh_token(
                    str(user.id), access_token_expire_time, role_ids=user_role_ids
                )
                login_logs_params = dict(
                    db=db, request=request, user=user, login_time=self.login_time, status=1, msg='登录成功'
                )
            except errors.NotFoundError as e:
                raise errors.NotFoundError(msg=e.msg)
            except errors.AuthorizationError as e:
                login_logs_params.update({'status': 0, 'msg': e.msg})
                background_tasks.add_task(LoginLogService.create, **login_logs_params)
                raise errors.AuthorizationError(msg=e.msg)
            except Exception as e:
                raise e
            else:
                background_tasks.add_task(LoginLogService.create, **login_logs_params)
                return access_token, refresh_token, access_token_expire_time, refresh_token_expire_time, user

    @staticmethod
    async def refresh_token(*, user_id: int, custom_time: RefreshTokenTime) -> tuple[str, datetime]:
        async with async_db_session() as db:
            current_user = await UserDao.get(db, user_id)
            if not current_user:
                raise errors.NotFoundError(msg='用户不存在')
            elif not current_user.is_active:
                raise errors.AuthorizationError(msg='用户已锁定, 获取失败')
            user_role_ids = await UserDao.get_role_ids(db, current_user.id)
            refresh_token, refresh_token_expire_time = await jwt.create_refresh_token(
                str(current_user.id), custom_expire_time=custom_time, role_ids=user_role_ids
            )
            return refresh_token, refresh_token_expire_time

    @staticmethod
    async def logout(user_id: int) -> NoReturn:
        key = f'{settings.TOKEN_REDIS_PREFIX}:{user_id}:'
        await redis_client.delete_prefix(key)

    @staticmethod
    async def register(obj: CreateUser) -> NoReturn:
        async with async_db_session.begin() as db:
            username = await UserDao.get_by_username(db, obj.username)
            if username:
                raise errors.ForbiddenError(msg='该用户名已注册')
            email = await UserDao.check_email(db, obj.email)
            if email:
                raise errors.ForbiddenError(msg='该邮箱已注册')
            try:
                validate_email(obj.email, check_deliverability=False).email
            except EmailNotValidError:
                raise errors.ForbiddenError(msg='邮箱格式错误')
            dept = await DeptDao.get(db, obj.dept_id)
            if not dept:
                raise errors.NotFoundError(msg='部门不存在')
            for role_id in obj.roles:
                role = await RoleDao.get(db, role_id)
                if not role:
                    raise errors.NotFoundError(msg='角色不存在')
            await UserDao.create(db, obj)

    @staticmethod
    async def pwd_reset(obj: ResetPassword) -> int:
        async with async_db_session.begin() as db:
            pwd1 = obj.password1
            pwd2 = obj.password2
            if pwd1 != pwd2:
                raise errors.ForbiddenError(msg='两次密码输入不一致')
            count = await UserDao.reset_password(db, obj.id, obj.password2)
            return count

    @staticmethod
    async def get_userinfo(username: str) -> User:
        async with async_db_session() as db:
            user = await UserDao.get_with_relation(db, username=username)
            if not user:
                raise errors.NotFoundError(msg='用户不存在')
            return user

    @staticmethod
    async def update(*, username: str, current_user: User, obj: UpdateUser) -> int:
        async with async_db_session.begin() as db:
            if not current_user.is_superuser:
                if not username == current_user.username:
                    raise errors.AuthorizationError
            input_user = await UserDao.get_with_relation(db, username=username)
            if not input_user:
                raise errors.NotFoundError(msg='用户不存在')
            if input_user.username != obj.username:
                username = await UserDao.get_by_username(db, obj.username)
                if username:
                    raise errors.ForbiddenError(msg='该用户名已存在')
            if input_user.email != obj.email:
                _email = await UserDao.check_email(db, obj.email)
                if _email:
                    raise errors.ForbiddenError(msg='该邮箱已注册')
                try:
                    validate_email(obj.email, check_deliverability=False).email
                except EmailNotValidError:
                    raise errors.ForbiddenError(msg='邮箱格式错误')
            if obj.phone is not None:
                if not re_verify.is_phone(obj.phone):
                    raise errors.ForbiddenError(msg='手机号码输入有误')
            dept = await DeptDao.get(db, obj.dept_id)
            if not dept:
                raise errors.NotFoundError(msg='部门不存在')
            for role_id in obj.roles:
                role = await RoleDao.get(db, role_id)
                if not role:
                    raise errors.NotFoundError(msg='角色不存在')
            count = await UserDao.update_userinfo(db, input_user, obj)
            return count

    @staticmethod
    async def update_avatar(*, username: str, current_user: User, avatar: Avatar) -> int:
        async with async_db_session.begin() as db:
            if not current_user.is_superuser:
                if not username == current_user.username:
                    raise errors.AuthorizationError
            input_user = await UserDao.get_by_username(db, username)
            if not input_user:
                raise errors.NotFoundError(msg='用户不存在')
            count = await UserDao.update_avatar(db, input_user, avatar)
            return count

    @staticmethod
    async def get_select() -> Select:
        return UserDao.get_all()

    @staticmethod
    async def update_permission(pk: int) -> int:
        async with async_db_session.begin() as db:
            if await UserDao.get(db, pk):
                count = await UserDao.set_super(db, pk)
                return count
            else:
                raise errors.NotFoundError(msg='用户不存在')

    @staticmethod
    async def update_active(pk: int) -> int:
        async with async_db_session.begin() as db:
            if await UserDao.get(db, pk):
                count = await UserDao.set_active(db, pk)
                return count
            else:
                raise errors.NotFoundError(msg='用户不存在')

    @staticmethod
    async def delete(*, username: str, current_user: User) -> int:
        async with async_db_session.begin() as db:
            if not current_user.is_superuser:
                if not username == current_user.username:
                    raise errors.AuthorizationError
            input_user = await UserDao.get_by_username(db, username)
            if not input_user:
                raise errors.NotFoundError(msg='用户不存在')
            count = await UserDao.delete(db, input_user.id)
            return count
