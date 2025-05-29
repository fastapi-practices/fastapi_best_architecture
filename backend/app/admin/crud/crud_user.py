#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import bcrypt

from sqlalchemy import and_, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import noload, selectinload
from sqlalchemy.sql import Select
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import Dept, Role, User
from backend.app.admin.schema.user import (
    AddUserParam,
    RegisterUserParam,
    UpdateUserParam,
)
from backend.common.security.jwt import get_hash_password
from backend.utils.timezone import timezone


class CRUDUser(CRUDPlus[User]):
    """用户数据库操作类"""

    async def get(self, db: AsyncSession, user_id: int) -> User | None:
        """
        获取用户详情

        :param db: 数据库会话
        :param user_id: 用户 ID
        :return:
        """
        return await self.select_model(db, user_id)

    async def get_by_username(self, db: AsyncSession, username: str) -> User | None:
        """
        通过用户名获取用户

        :param db: 数据库会话
        :param username: 用户名
        :return:
        """
        return await self.select_model_by_column(db, username=username)

    async def get_by_nickname(self, db: AsyncSession, nickname: str) -> User | None:
        """
        通过昵称获取用户

        :param db: 数据库会话
        :param nickname: 用户昵称
        :return:
        """
        return await self.select_model_by_column(db, nickname=nickname)

    async def update_login_time(self, db: AsyncSession, username: str) -> int:
        """
        更新用户最后登录时间

        :param db: 数据库会话
        :param username: 用户名
        :return:
        """
        return await self.update_model_by_column(db, {'last_login_time': timezone.now()}, username=username)

    async def create(self, db: AsyncSession, obj: RegisterUserParam, *, social: bool = False) -> None:
        """
        创建用户

        :param db: 数据库会话
        :param obj: 注册用户参数
        :param social: 是否社交用户
        :return:
        """
        if not social:
            salt = bcrypt.gensalt()
            obj.password = get_hash_password(obj.password, salt)
            dict_obj = obj.model_dump()
            dict_obj.update({'is_staff': True, 'salt': salt})
        else:
            dict_obj = obj.model_dump()
            dict_obj.update({'is_staff': True, 'salt': None})
        new_user = self.model(**dict_obj)
        db.add(new_user)

    async def add(self, db: AsyncSession, obj: AddUserParam) -> None:
        """
        添加用户

        :param db: 数据库会话
        :param obj: 添加用户参数
        :return:
        """
        salt = bcrypt.gensalt()
        obj.password = get_hash_password(obj.password, salt)
        dict_obj = obj.model_dump(exclude={'roles'})
        dict_obj.update({'salt': salt})
        new_user = self.model(**dict_obj)

        stmt = select(Role).where(Role.id.in_(obj.roles))
        roles = await db.execute(stmt)
        new_user.roles = roles.scalars().all()

        db.add(new_user)

    async def update(self, db: AsyncSession, input_user: User, obj: UpdateUserParam) -> int:
        """
        更新用户信息

        :param db: 数据库会话
        :param input_user: 用户 ID
        :param obj: 更新用户参数
        :return:
        """
        role_ids = obj.roles
        del obj.roles
        count = await self.update_model(db, input_user.id, obj)

        stmt = select(Role).where(Role.id.in_(role_ids))
        roles = await db.execute(stmt)
        input_user.roles = roles.scalars().all()
        return count

    async def delete(self, db: AsyncSession, user_id: int) -> int:
        """
        删除用户

        :param db: 数据库会话
        :param user_id: 用户 ID
        :return:
        """
        return await self.delete_model(db, user_id)

    async def check_email(self, db: AsyncSession, email: str) -> User | None:
        """
        检查邮箱是否已被注册

        :param db: 数据库会话
        :param email: 电子邮箱
        :return:
        """
        return await self.select_model_by_column(db, email=email)

    async def reset_password(self, db: AsyncSession, pk: int, new_pwd: str) -> int:
        """
        重置用户密码

        :param db: 数据库会话
        :param pk: 用户 ID
        :param new_pwd: 新密码（已加密）
        :return:
        """
        return await self.update_model(db, pk, {'password': new_pwd})

    async def get_list(self, dept: int | None, username: str | None, phone: str | None, status: int | None) -> Select:
        """
        获取用户列表

        :param dept: 部门 ID
        :param username: 用户名
        :param phone: 电话号码
        :param status: 用户状态
        :return:
        """
        stmt = (
            select(self.model)
            .options(
                selectinload(self.model.dept).options(noload(Dept.parent), noload(Dept.children), noload(Dept.users)),
                selectinload(self.model.roles).options(noload(Role.users), noload(Role.menus), noload(Role.scopes)),
            )
            .order_by(desc(self.model.join_time))
        )

        filters = []
        if dept:
            filters.append(self.model.dept_id == dept)
        if username:
            filters.append(self.model.username.like(f'%{username}%'))
        if phone:
            filters.append(self.model.phone.like(f'%{phone}%'))
        if status is not None:
            filters.append(self.model.status == status)

        if filters:
            stmt = stmt.where(and_(*filters))

        return stmt

    async def get_super(self, db: AsyncSession, user_id: int) -> bool:
        """
        获取用户是否为超级管理员

        :param db: 数据库会话
        :param user_id: 用户 ID
        :return:
        """
        user = await self.get(db, user_id)
        return user.is_superuser

    async def get_staff(self, db: AsyncSession, user_id: int) -> bool:
        """
        获取用户是否可以登录后台

        :param db: 数据库会话
        :param user_id: 用户 ID
        :return:
        """
        user = await self.get(db, user_id)
        return user.is_staff

    async def get_status(self, db: AsyncSession, user_id: int) -> int:
        """
        获取用户状态

        :param db: 数据库会话
        :param user_id: 用户 ID
        :return:
        """
        user = await self.get(db, user_id)
        return user.status

    async def get_multi_login(self, db: AsyncSession, user_id: int) -> bool:
        """
        获取用户是否允许多端登录

        :param db: 数据库会话
        :param user_id: 用户 ID
        :return:
        """
        user = await self.get(db, user_id)
        return user.is_multi_login

    async def set_super(self, db: AsyncSession, user_id: int, is_super: bool) -> int:
        """
        设置用户超级管理员状态

        :param db: 数据库会话
        :param user_id: 用户 ID
        :param is_super: 是否超级管理员
        :return:
        """
        return await self.update_model(db, user_id, {'is_superuser': is_super})

    async def set_staff(self, db: AsyncSession, user_id: int, is_staff: bool) -> int:
        """
        设置用户后台登录状态

        :param db: 数据库会话
        :param user_id: 用户 ID
        :param is_staff: 是否可登录后台
        :return:
        """
        return await self.update_model(db, user_id, {'is_staff': is_staff})

    async def set_status(self, db: AsyncSession, user_id: int, status: int) -> int:
        """
        设置用户状态

        :param db: 数据库会话
        :param user_id: 用户 ID
        :param status: 状态
        :return:
        """
        return await self.update_model(db, user_id, {'status': status})

    async def set_multi_login(self, db: AsyncSession, user_id: int, multi_login: bool) -> int:
        """
        设置用户多端登录状态

        :param db: 数据库会话
        :param user_id: 用户 ID
        :param multi_login: 是否允许多端登录
        :return:
        """
        return await self.update_model(db, user_id, {'is_multi_login': multi_login})

    async def get_with_relation(
        self, db: AsyncSession, *, user_id: int | None = None, username: str | None = None
    ) -> User | None:
        """
        获取用户关联信息

        :param db: 数据库会话
        :param user_id: 用户 ID
        :param username: 用户名
        :return:
        """
        stmt = select(self.model).options(
            selectinload(self.model.dept),
            selectinload(self.model.roles).options(selectinload(Role.menus), selectinload(Role.scopes)),
        )

        filters = []
        if user_id:
            filters.append(self.model.id == user_id)
        if username:
            filters.append(self.model.username == username)

        if filters:
            stmt = stmt.where(and_(*filters))

        user = await db.execute(stmt)
        return user.scalars().first()


user_dao: CRUDUser = CRUDUser(User)
