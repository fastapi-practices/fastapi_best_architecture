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
from backend.common.enums import UserPermissionType
from backend.common.exception import errors
from backend.common.security.jwt import get_hash_password, get_token, jwt_decode, password_verify, superuser_verify
from backend.core.conf import settings
from backend.database.db import async_db_session
from backend.database.redis import redis_client


class UserService:
    """用户服务类"""

    @staticmethod
    async def get_userinfo(*, pk: int | None = None, username: str | None = None) -> User:
        """
        获取用户信息

        :param pk: 用户 ID
        :param username: 用户名
        :return:
        """
        async with async_db_session() as db:
            user = await user_dao.get_with_relation(db, user_id=pk, username=username)
            if not user:
                raise errors.NotFoundError(msg='用户不存在')
            return user

    @staticmethod
    async def get_roles(*, pk: int) -> Sequence[Role]:
        """
        获取用户所有角色

        :param pk: 用户 ID
        :return:
        """
        async with async_db_session() as db:
            user = await user_dao.get_with_relation(db, user_id=pk)
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
    async def create(*, request: Request, obj: AddUserParam) -> None:
        """
        创建用户

        :param request: FastAPI 请求对象
        :param obj: 用户添加参数
        :return:
        """
        async with async_db_session.begin() as db:
            superuser_verify(request)
            if await user_dao.get_by_username(db, obj.username):
                raise errors.ConflictError(msg='用户名已注册')
            obj.nickname = obj.nickname if obj.nickname else f'#{random.randrange(88888, 99999)}'
            if not obj.password:
                raise errors.RequestError(msg='密码不允许为空')
            if not await dept_dao.get(db, obj.dept_id):
                raise errors.NotFoundError(msg='部门不存在')
            for role_id in obj.roles:
                if not await role_dao.get(db, role_id):
                    raise errors.NotFoundError(msg='角色不存在')
            await user_dao.add(db, obj)

    @staticmethod
    async def update(*, request: Request, pk: int, obj: UpdateUserParam) -> int:
        """
        更新用户信息

        :param request: FastAPI 请求对象
        :param pk: 用户 ID
        :param obj: 用户更新参数
        :return:
        """
        async with async_db_session.begin() as db:
            user = await user_dao.get_with_relation(db, user_id=pk)
            if not user:
                raise errors.NotFoundError(msg='用户不存在')
            if request.user.username != user.username:
                raise errors.ForbiddenError(msg='只能修改自己的信息')
            if obj.username != user.username:
                if await user_dao.get_by_username(db, obj.username):
                    raise errors.ConflictError(msg='用户名已注册')
            for role_id in obj.roles:
                if not await role_dao.get(db, role_id):
                    raise errors.NotFoundError(msg='角色不存在')
            count = await user_dao.update(db, user, obj)
            await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{user.id}')
            return count

    @staticmethod
    async def update_superuser(*, request: Request, pk: int) -> int:
        """
        更新用户管理员状态

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
                raise errors.ForbiddenError(msg='禁止修改自身权限')
            count = await user_dao.set_super(db, pk, not user.status)
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
                raise errors.ForbiddenError(msg='禁止修改自身权限')
            count = await user_dao.set_staff(db, pk, not user.is_staff)
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
                raise errors.ForbiddenError(msg='禁止修改自身权限')
            count = await user_dao.set_status(db, pk, 0 if user.status == 1 else 1)
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
            multi_login = user.is_multi_login if pk != user.id else request.user.is_multi_login
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

    async def update_permission(self, *, request: Request, pk: int, type: UserPermissionType) -> int:
        """
        更新用户权限

        :param request: FastAPI 请求对象
        :param pk: 用户 ID
        :param type: 权限类型
        :return:
        """
        match type:
            case UserPermissionType.superuser:
                count = await self.update_superuser(request=request, pk=pk)
            case UserPermissionType.staff:
                count = await self.update_staff(request=request, pk=pk)
            case UserPermissionType.status:
                count = await self.update_status(request=request, pk=pk)
            case UserPermissionType.multi_login:
                count = await self.update_multi_login(request=request, pk=pk)
            case _:
                raise errors.RequestError(msg='权限类型不存在')
        return count

    @staticmethod
    async def reset_pwd(*, pk: int, obj: ResetPasswordParam) -> int:
        """
        重置用户密码

        :param pk: 用户 ID
        :param obj: 密码重置参数
        :return:
        """
        async with async_db_session.begin() as db:
            user = await user_dao.get(db, pk)
            if not user:
                raise errors.NotFoundError(msg='用户不存在')
            if not password_verify(obj.old_password, user.password):
                raise errors.RequestError(msg='原密码错误')
            if obj.new_password != obj.confirm_password:
                raise errors.RequestError(msg='密码输入不一致')
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
    async def delete(*, pk: int) -> int:
        """
        删除用户

        :param pk: 用户 ID
        :return:
        """
        async with async_db_session.begin() as db:
            user = await user_dao.get(db, pk)
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
