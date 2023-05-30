#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import NoReturn

from email_validator import validate_email, EmailNotValidError
from fastapi import Request
from sqlalchemy import Select

from backend.app.common.exception import errors
from backend.app.common.jwt import get_token, jwt_decode
from backend.app.common.redis import redis_client
from backend.app.core.conf import settings
from backend.app.crud.crud_dept import DeptDao
from backend.app.crud.crud_role import RoleDao
from backend.app.crud.crud_user import UserDao
from backend.app.database.db_mysql import async_db_session
from backend.app.models import User
from backend.app.schemas.user import CreateUser, ResetPassword, UpdateUser, Avatar
from backend.app.utils import re_verify


class UserService:
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
    async def get_select(*, username: str = None, phone: str = None, status: bool = None) -> Select:
        return await UserDao.get_all(username=username, phone=phone, status=status)

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
    async def update_multi_login(*, request: Request, pk: int, current_user: User) -> int:
        async with async_db_session.begin() as db:
            if not current_user.is_superuser:
                if not pk == current_user.id:
                    raise errors.AuthorizationError
            if await UserDao.get(db, pk):
                count = await UserDao.set_multi_login(db, pk)
                token = get_token(request)
                user_id, role_ids = jwt_decode(token)
                latest_multi_login = await UserDao.get_multi_login(db, pk)
                if pk == user_id:
                    if not latest_multi_login:
                        prefix = f'{settings.TOKEN_REDIS_PREFIX}:{pk}:'
                        await redis_client.delete_prefix(prefix, exclude=prefix + token)
                else:
                    if not latest_multi_login:
                        prefix = f'{settings.TOKEN_REDIS_PREFIX}:{pk}:'
                        await redis_client.delete_prefix(prefix)
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
            prefix = [
                f'{settings.TOKEN_REDIS_PREFIX}:{current_user.id}:',
                f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{current_user.id}:',
            ]
            for i in prefix:
                await redis_client.delete_prefix(i)
            return count
