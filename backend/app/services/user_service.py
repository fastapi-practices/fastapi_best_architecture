#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random

from fastapi import Request
from sqlalchemy import Select

from backend.app.common.exception import errors
from backend.app.common.jwt import get_token, password_verify, superuser_verify
from backend.app.common.redis import redis_client
from backend.app.core.conf import settings
from backend.app.crud.crud_dept import DeptDao
from backend.app.crud.crud_role import RoleDao
from backend.app.crud.crud_user import UserDao
from backend.app.database.db_mysql import async_db_session
from backend.app.models import User
from backend.app.schemas.user import AddUser, Avatar, RegisterUser, ResetPassword, UpdateUser, UpdateUserRole


class UserService:
    @staticmethod
    async def register(*, obj: RegisterUser) -> None:
        async with async_db_session.begin() as db:
            username = await UserDao.get_by_username(db, obj.username)
            if username:
                raise errors.ForbiddenError(msg='该用户名已注册')
            obj.nickname = obj.nickname if obj.nickname else f'用户{random.randrange(10000, 99999)}'
            nickname = await UserDao.get_by_nickname(db, obj.nickname)
            if nickname:
                raise errors.ForbiddenError(msg='昵称已注册')
            email = await UserDao.check_email(db, obj.email)
            if email:
                raise errors.ForbiddenError(msg='该邮箱已注册')
            await UserDao.create(db, obj)

    @staticmethod
    async def add(*, obj: AddUser) -> None:
        async with async_db_session.begin() as db:
            username = await UserDao.get_by_username(db, obj.username)
            if username:
                raise errors.ForbiddenError(msg='此用户名已注册')
            obj.nickname = obj.nickname if obj.nickname else f'用户{random.randrange(10000, 99999)}'
            nickname = await UserDao.get_by_nickname(db, obj.nickname)
            if nickname:
                raise errors.ForbiddenError(msg='昵称已注册')
            dept = await DeptDao.get(db, obj.dept_id)
            if not dept:
                raise errors.NotFoundError(msg='部门不存在')
            for role_id in obj.roles:
                role = await RoleDao.get(db, role_id)
                if not role:
                    raise errors.NotFoundError(msg='角色不存在')
            email = await UserDao.check_email(db, obj.email)
            if email:
                raise errors.ForbiddenError(msg='该邮箱已注册')
            await UserDao.add(db, obj)

    @staticmethod
    async def pwd_reset(*, request: Request, obj: ResetPassword) -> int:
        async with async_db_session.begin() as db:
            op = obj.old_password
            if not await password_verify(op + request.user.salt, request.user.password):
                raise errors.ForbiddenError(msg='旧密码错误')
            np1 = obj.new_password
            np2 = obj.confirm_password
            if np1 != np2:
                raise errors.ForbiddenError(msg='两次密码输入不一致')
            count = await UserDao.reset_password(db, request.user.id, obj.new_password, request.user.salt)
            prefix = [
                f'{settings.TOKEN_REDIS_PREFIX}:{request.user.id}:',
                f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{request.user.id}:',
            ]
            for i in prefix:
                await redis_client.delete_prefix(i)
            return count

    @staticmethod
    async def get_userinfo(*, username: str) -> User:
        async with async_db_session() as db:
            user = await UserDao.get_with_relation(db, username=username)
            if not user:
                raise errors.NotFoundError(msg='用户不存在')
            return user

    @staticmethod
    async def update(*, request: Request, username: str, obj: UpdateUser) -> int:
        async with async_db_session.begin() as db:
            await superuser_verify(request)
            input_user = await UserDao.get_with_relation(db, username=username)
            if not input_user:
                raise errors.NotFoundError(msg='用户不存在')
            if input_user.username != obj.username:
                _username = await UserDao.get_by_username(db, obj.username)
                if _username:
                    raise errors.ForbiddenError(msg='该用户名已存在')
            if input_user.nickname != obj.nickname:
                nickname = await UserDao.get_by_nickname(db, obj.nickname)
                if nickname:
                    raise errors.ForbiddenError(msg='改昵称已存在')
            if input_user.email != obj.email:
                email = await UserDao.check_email(db, obj.email)
                if email:
                    raise errors.ForbiddenError(msg='该邮箱已注册')
            count = await UserDao.update_userinfo(db, input_user, obj)
            return count

    @staticmethod
    async def update_role(*, request: Request, username: str, obj: UpdateUserRole) -> None:
        async with async_db_session.begin() as db:
            if not request.user.is_superuser:
                if request.user.username != username:
                    raise errors.ForbiddenError(msg='你只能修改自己的角色')
            input_user = await UserDao.get_with_relation(db, username=username)
            if not input_user:
                raise errors.NotFoundError(msg='用户不存在')
            for role_id in obj.roles:
                role = await RoleDao.get(db, role_id)
                if not role:
                    raise errors.NotFoundError(msg='角色不存在')
            await UserDao.update_role(db, input_user, obj)

    @staticmethod
    async def update_avatar(*, request: Request, username: str, avatar: Avatar) -> int:
        async with async_db_session.begin() as db:
            if not request.user.is_superuser:
                if request.user.username != username:
                    raise errors.ForbiddenError(msg='你只能修改自己的头像')
            input_user = await UserDao.get_by_username(db, username)
            if not input_user:
                raise errors.NotFoundError(msg='用户不存在')
            count = await UserDao.update_avatar(db, input_user, avatar)
            return count

    @staticmethod
    async def get_select(*, dept: int, username: str = None, phone: str = None, status: int = None) -> Select:
        return await UserDao.get_all(dept=dept, username=username, phone=phone, status=status)

    @staticmethod
    async def update_permission(*, request: Request, pk: int) -> int:
        async with async_db_session.begin() as db:
            await superuser_verify(request)
            if not await UserDao.get(db, pk):
                raise errors.NotFoundError(msg='用户不存在')
            else:
                if pk == request.user.id:
                    raise errors.ForbiddenError(msg='禁止修改自身管理员权限')
                count = await UserDao.set_super(db, pk)
                return count

    @staticmethod
    async def update_staff(*, request: Request, pk: int) -> int:
        async with async_db_session.begin() as db:
            await superuser_verify(request)
            if not await UserDao.get(db, pk):
                raise errors.NotFoundError(msg='用户不存在')
            else:
                if pk == request.user.id:
                    raise errors.ForbiddenError(msg='禁止修改自身后台管理登陆权限')
                count = await UserDao.set_staff(db, pk)
                return count

    @staticmethod
    async def update_status(*, request: Request, pk: int) -> int:
        async with async_db_session.begin() as db:
            await superuser_verify(request)
            if not await UserDao.get(db, pk):
                raise errors.NotFoundError(msg='用户不存在')
            else:
                if pk == request.user.id:
                    raise errors.ForbiddenError(msg='禁止修改自身状态')
                count = await UserDao.set_status(db, pk)
                return count

    @staticmethod
    async def update_multi_login(*, request: Request, pk: int) -> int:
        async with async_db_session.begin() as db:
            await superuser_verify(request)
            if not await UserDao.get(db, pk):
                raise errors.NotFoundError(msg='用户不存在')
            else:
                count = await UserDao.set_multi_login(db, pk)
                token = await get_token(request)
                user_id = request.user.id
                latest_multi_login = await UserDao.get_multi_login(db, pk)
                # TODO: 删除用户 refresh token, 此操作需要传参，暂时不考虑实现
                # 当前用户修改自身时（普通/超级），除当前token外，其他token失效
                if pk == user_id:
                    if not latest_multi_login:
                        prefix = f'{settings.TOKEN_REDIS_PREFIX}:{pk}:'
                        await redis_client.delete_prefix(prefix, exclude=prefix + token)
                # 超级用户修改他人时，他人token将全部失效
                else:
                    if not latest_multi_login:
                        prefix = f'{settings.TOKEN_REDIS_PREFIX}:{pk}:'
                        await redis_client.delete_prefix(prefix)
                return count

    @staticmethod
    async def delete(*, request: Request, username: str) -> int:
        async with async_db_session.begin() as db:
            await superuser_verify(request)
            input_user = await UserDao.get_by_username(db, username)
            if not input_user:
                raise errors.NotFoundError(msg='用户不存在')
            count = await UserDao.delete(db, input_user.id)
            prefix = [
                f'{settings.TOKEN_REDIS_PREFIX}:{input_user.id}:',
                f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{input_user.id}:',
            ]
            for i in prefix:
                await redis_client.delete_prefix(i)
            return count
