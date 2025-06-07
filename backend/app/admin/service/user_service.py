#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random

from typing import Sequence

from fastapi import Request
from sqlalchemy import Select

from backend.app.admin.crud.crud_dept import dept_dao
from backend.app.admin.crud.crud_role import role_dao
from backend.app.admin.crud.crud_user import user_dao
from backend.app.admin.model import Role, User
from backend.app.admin.schema.user import (
    AddUserParam,
    ResetPasswordParam,
    UpdateUserParam,
)
from backend.common.exception import errors
from backend.common.security.jwt import get_hash_password, get_token, jwt_decode, password_verify, superuser_verify
from backend.core.conf import settings
from backend.database.db import async_db_session
from backend.database.redis import redis_client


class UserService:
    """用户服务类"""

    @staticmethod
    async def add(*, request: Request, obj: AddUserParam) -> None:
        """
        添加新用户

        :param request: FastAPI 请求对象
        :param obj: 用户添加参数
        :return:
        """
        async with async_db_session.begin() as db:
            superuser_verify(request)
            username = await user_dao.get_by_username(db, obj.username)
            if username:
                raise errors.ForbiddenError(msg='用户已注册')
            obj.nickname = obj.nickname if obj.nickname else f'#{random.randrange(88888, 99999)}'
            nickname = await user_dao.get_by_nickname(db, obj.nickname)
            if nickname:
                raise errors.ForbiddenError(msg='昵称已注册')
            if not obj.password:
                raise errors.ForbiddenError(msg='密码为空')
            dept = await dept_dao.get(db, obj.dept_id)
            if not dept:
                raise errors.NotFoundError(msg='部门不存在')
            for role_id in obj.roles:
                role = await role_dao.get(db, role_id)
                if not role:
                    raise errors.NotFoundError(msg='角色不存在')
            await user_dao.add(db, obj)

    @staticmethod
    async def pwd_reset(*, username: str, obj: ResetPasswordParam) -> int:
        """
        重置用户密码

        :param username: 用户名
        :param obj: 密码重置参数
        :return:
        """
        async with async_db_session.begin() as db:
            user = await user_dao.get_by_username(db, username)
            if not user:
                raise errors.NotFoundError(msg='用户不存在')
            if not password_verify(obj.old_password, user.password):
                raise errors.ForbiddenError(msg='原密码错误')
            if obj.new_password != obj.confirm_password:
                raise errors.ForbiddenError(msg='密码输入不一致')
            new_pwd = get_hash_password(obj.new_password, user.salt)
            count = await user_dao.reset_password(db, user.id, new_pwd)
            key_prefix = [
                f'{settings.TOKEN_REDIS_PREFIX}:{user.id}',
                f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{user.id}',
                f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}',
            ]
            for prefix in key_prefix:
                await redis_client.delete_prefix(prefix)
            return count

    @staticmethod
    async def get_userinfo(*, username: str) -> User:
        """
        获取用户信息

        :param username: 用户名
        :return:
        """
        async with async_db_session() as db:
            user = await user_dao.get_with_relation(db, username=username)
            if not user:
                raise errors.NotFoundError(msg='用户不存在')
            return user

    @staticmethod
    async def get_roles(*, username: str) -> Sequence[Role]:
        """
        获取用户所有角色

        :param username: 用户名
        :return:
        """
        async with async_db_session() as db:
            user = await user_dao.get_with_relation(db, username=username)
            if not user:
                raise errors.NotFoundError(msg='用户不存在')
            return user.roles

    @staticmethod
    async def get_select(*, dept: int, username: str, phone: str, status: int) -> Select:
        """
        获取用户列表查询条件

        :param dept: 部门 ID
        :param username: 用户名
        :param phone: 手机号
        :param status: 状态
        :return:
        """
        return await user_dao.get_list(dept=dept, username=username, phone=phone, status=status)

    @staticmethod
    async def update(*, request: Request, username: str, obj: UpdateUserParam) -> int:
        """
        更新用户信息

        :param request: FastAPI 请求对象
        :param username: 用户名
        :param obj: 用户更新参数
        :return:
        """
        async with async_db_session.begin() as db:
            if request.user.username != username:
                raise errors.ForbiddenError(msg='你只能修改自己的信息')
            user = await user_dao.get_with_relation(db, username=username)
            if not user:
                raise errors.NotFoundError(msg='用户不存在')
            if user.username != obj.username:
                _username = await user_dao.get_by_username(db, obj.username)
                if _username:
                    raise errors.ForbiddenError(msg='用户名已注册')
            if user.nickname != obj.nickname:
                nickname = await user_dao.get_by_nickname(db, obj.nickname)
                if nickname:
                    raise errors.ForbiddenError(msg='昵称已注册')
            for role_id in obj.roles:
                role = await role_dao.get(db, role_id)
                if not role:
                    raise errors.NotFoundError(msg='角色不存在')
            count = await user_dao.update(db, user, obj)
            await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
            return count

    @staticmethod
    async def update_permission(*, request: Request, pk: int) -> int:
        """
        更新用户权限

        :param request: FastAPI 请求对象
        :param pk: 用户 ID
        :return:
        """
        async with async_db_session.begin() as db:
            superuser_verify(request)
            user = await user_dao.get(db, pk)
            if not user:
                raise errors.NotFoundError(msg='用户不存在')
            if pk == request.user.id:
                raise errors.ForbiddenError(msg='非法操作')
            super_status = await user_dao.get_super(db, pk)
            count = await user_dao.set_super(db, pk, not super_status)
            await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
            return count

    @staticmethod
    async def update_staff(*, request: Request, pk: int) -> int:
        """
        更新用户职员状态

        :param request: FastAPI 请求对象
        :param pk: 用户 ID
        :return:
        """
        async with async_db_session.begin() as db:
            superuser_verify(request)
            user = await user_dao.get(db, pk)
            if not user:
                raise errors.NotFoundError(msg='用户不存在')
            if pk == request.user.id:
                raise errors.ForbiddenError(msg='非法操作')
            staff_status = await user_dao.get_staff(db, pk)
            count = await user_dao.set_staff(db, pk, not staff_status)
            await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
            return count

    @staticmethod
    async def update_status(*, request: Request, pk: int) -> int:
        """
        更新用户状态

        :param request: FastAPI 请求对象
        :param pk: 用户 ID
        :return:
        """
        async with async_db_session.begin() as db:
            superuser_verify(request)
            user = await user_dao.get(db, pk)
            if not user:
                raise errors.NotFoundError(msg='用户不存在')
            if pk == request.user.id:
                raise errors.ForbiddenError(msg='非法操作')
            status = await user_dao.get_status(db, pk)
            count = await user_dao.set_status(db, pk, 0 if status == 1 else 1)
            await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
            return count

    @staticmethod
    async def update_multi_login(*, request: Request, pk: int) -> int:
        """
        更新用户多端登录状态

        :param request: FastAPI 请求对象
        :param pk: 用户 ID
        :return:
        """
        async with async_db_session.begin() as db:
            superuser_verify(request)
            user = await user_dao.get(db, pk)
            if not user:
                raise errors.NotFoundError(msg='用户不存在')
            multi_login = await user_dao.get_multi_login(db, pk) if pk != user.id else request.user.is_multi_login
            new_multi_login = not multi_login
            count = await user_dao.set_multi_login(db, pk, new_multi_login)
            await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
            token = get_token(request)
            token_payload = jwt_decode(token)
            if pk == user.id:
                # 系统管理员修改自身时，除当前 token 外，其他 token 失效
                if not new_multi_login:
                    key_prefix = f'{settings.TOKEN_REDIS_PREFIX}:{user.id}'
                    await redis_client.delete_prefix(key_prefix, exclude=f'{key_prefix}:{token_payload.session_uuid}')
            else:
                # 系统管理员修改他人时，他人 token 全部失效
                if not new_multi_login:
                    key_prefix = f'{settings.TOKEN_REDIS_PREFIX}:{user.id}'
                    await redis_client.delete_prefix(key_prefix)
            return count

    @staticmethod
    async def delete(*, username: str) -> int:
        """
        删除用户

        :param username: 用户名
        :return:
        """
        async with async_db_session.begin() as db:
            user = await user_dao.get_by_username(db, username)
            if not user:
                raise errors.NotFoundError(msg='用户不存在')
            count = await user_dao.delete(db, user.id)
            key_prefix = [
                f'{settings.TOKEN_REDIS_PREFIX}:{user.id}',
                f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{user.id}',
            ]
            for key in key_prefix:
                await redis_client.delete_prefix(key)
            return count


user_service: UserService = UserService()
