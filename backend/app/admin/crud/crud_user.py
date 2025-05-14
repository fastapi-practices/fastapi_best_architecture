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
    AvatarParam,
    RegisterUserParam,
    UpdateUserParam,
    UpdateUserRoleParam,
)
from backend.common.security.jwt import get_hash_password
from backend.utils.timezone import timezone


class CRUDUser(CRUDPlus[User]):
    """User database operating class"""

    async def get(self, db: AsyncSession, user_id: int) -> User | None:
        """
        Get User Details

        :param db: database session
        :param user_id: userID
        :return:
        """
        return await self.select_model(db, user_id)

    async def get_by_username(self, db: AsyncSession, username: str) -> User | None:
        """
        Getting users through a user name

        :param db: database session
        :param username:
        :return:
        """
        return await self.select_model_by_column(db, username=username)

    async def get_by_nickname(self, db: AsyncSession, nickname: str) -> User | None:
        """
        Fetch users by nickname

        :param db: database session
        :param nickname:
        :return:
        """
        return await self.select_model_by_column(db, nickname=nickname)

    async def update_login_time(self, db: AsyncSession, username: str) -> int:
        """
        Update user last login time

        :param db: database session
        :param username:
        :return:
        """
        return await self.update_model_by_column(db, {'last_login_time': timezone.now()}, username=username)

    async def create(self, db: AsyncSession, obj: RegisterUserParam, *, social: bool = False) -> None:
        """
        Create User

        :param db: database session
        :param obj: register user parameters
        :param social: social users
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
        Add User

        :param db: database session
        :param obj: add user parameters
        :return:
        """
        salt = bcrypt.gensalt()
        obj.password = get_hash_password(obj.password, salt)
        dict_obj = obj.model_dump(exclude={'roles'})
        dict_obj.update({'salt': salt})
        new_user = self.model(**dict_obj)

        role_list = []
        for role_id in obj.roles:
            role_list.append(await db.get(Role, role_id))
        new_user.roles.extend(role_list)

        db.add(new_user)

    async def update_userinfo(self, db: AsyncSession, input_user: int, obj: UpdateUserParam) -> int:
        """
        Update user information

        :param db: database session
        :param input_user: user ID
        :param obj: update user parameters
        :return:
        """
        return await self.update_model(db, input_user, obj)

    @staticmethod
    async def update_role(db: AsyncSession, input_user: User, obj: UpdateUserRoleParam) -> None:
        """
        Update user roles

        :param db: database session
        :param input_user: user objects
        :param obj: update role parameters
        :return:
        """
        for i in list(input_user.roles):
            input_user.roles.remove(i)

        role_list = []
        for role_id in obj.roles:
            role_list.append(await db.get(Role, role_id))
        input_user.roles.extend(role_list)

    async def update_avatar(self, db: AsyncSession, input_user: int, avatar: AvatarParam) -> int:
        """
        Update user header

        :param db: database session
        :param input_user: user ID
        :param image address
        :return:
        """
        return await self.update_model(db, input_user, {'avatar': str(avatar.url)})

    async def delete(self, db: AsyncSession, user_id: int) -> int:
        """
        Remove User

        :param db: database session
        :param user_id: userID
        :return:
        """
        return await self.delete_model(db, user_id)

    async def check_email(self, db: AsyncSession, email: str) -> User | None:
        """
        Check if the mailbox is registered

        :param db: database session
        :param email: e-mail
        :return:
        """
        return await self.select_model_by_column(db, email=email)

    async def reset_password(self, db: AsyncSession, pk: int, new_pwd: str) -> int:
        """
        Reset user password

        :param db: database session
        :param pk: User ID
        :param new_pwd: new password (encrypted)
        :return:
        """
        return await self.update_model(db, pk, {'password': new_pwd})

    async def get_list(self, dept: int | None, username: str | None, phone: str | None, status: int | None) -> Select:
        """
        Get User List

        :param dept: Department ID
        :param username:
        :param phone number
        :param status: user status
        :return:
        """
        stmt = (
            select(self.model)
            .options(
                selectinload(self.model.dept).options(noload(Dept.parent), noload(Dept.children), noload(Dept.users)),
                noload(self.model.socials),
                selectinload(self.model.roles).options(noload(Role.users), noload(Role.menus), noload(Role.rules)),
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
        Retrieving whether the user is a super administrator

        :param db: database session
        :param user_id: userID
        :return:
        """
        user = await self.get(db, user_id)
        return user.is_superuser

    async def get_staff(self, db: AsyncSession, user_id: int) -> bool:
        """
        Retrieving user login backstage

        :param db: database session
        :param user_id: userID
        :return:
        """
        user = await self.get(db, user_id)
        return user.is_staff

    async def get_status(self, db: AsyncSession, user_id: int) -> int:
        """
        Get User Status

        :param db: database session
        :param user_id: userID
        :return:
        """
        user = await self.get(db, user_id)
        return user.status

    async def get_multi_login(self, db: AsyncSession, user_id: int) -> bool:
        """
        Retrieving user permission for multiple login

        :param db: database session
        :param user_id: userID
        :return:
        """
        user = await self.get(db, user_id)
        return user.is_multi_login

    async def set_super(self, db: AsyncSession, user_id: int, is_super: bool) -> int:
        """
        Setup User SuperAdminister Status

        :param db: database session
        :param user_id: userID
        :param is_supper: is the super administrator
        :return:
        """
        return await self.update_model(db, user_id, {'is_superuser': is_super})

    async def set_staff(self, db: AsyncSession, user_id: int, is_staff: bool) -> int:
        """
        Set user background login status

        :param db: database session
        :param user_id: userID
        :param is_staff: whether to log in backstage
        :return:
        """
        return await self.update_model(db, user_id, {'is_staff': is_staff})

    async def set_status(self, db: AsyncSession, user_id: int, status: int) -> int:
        """
        Set User Status

        :param db: database session
        :param user_id: userID
        :param status: status
        :return:
        """
        return await self.update_model(db, user_id, {'status': status})

    async def set_multi_login(self, db: AsyncSession, user_id: int, multi_login: bool) -> int:
        """
        Set user multi-end login status

        :param db: database session
        :param user_id: userID
        :param muldi_login: whether multiple login is allowed
        :return:
        """
        return await self.update_model(db, user_id, {'is_multi_login': multi_login})

    async def get_with_relation(
        self, db: AsyncSession, *, user_id: int | None = None, username: str | None = None
    ) -> User | None:
        """
        Get User Link Information

        :param db: database session
        :param user_id: userID
        :param username:
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
