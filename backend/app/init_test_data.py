#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio

from email_validator import EmailNotValidError, validate_email
from faker import Faker

from backend.app.api.jwt import get_hash_password
from backend.app.common.log import log
from backend.app.database.db_mysql import async_db_session
from backend.app.models import User


class InitData:
    """ 初始化数据 """

    def __init__(self):
        self.fake = Faker('zh_CN')

    @staticmethod
    async def create_superuser_by_yourself():
        """ 手动创建管理员账户 """
        print('请输入用户名:')
        username = input()
        print('请输入密码:')
        password = input()
        print('请输入邮箱:')
        while True:
            email = input()
            try:
                validate_email(email, check_deliverability=False).email
            except EmailNotValidError:
                print('邮箱不符合规范，请重新输入：')
                continue
            break
        user_obj = User(
            username=username,
            password=get_hash_password(password),
            email=email,
            is_superuser=True,
        )
        async with async_db_session.begin() as db:
            db.add(user_obj)
        log.info(f'管理员用户创建成功，账号：{username}，密码：{password}')

    async def fake_user(self):
        """ 自动创建普通用户 """
        username = self.fake.user_name()
        password = self.fake.password()
        email = self.fake.email()
        user_obj = User(
            username=username,
            password=get_hash_password(password),
            email=email,
            is_superuser=False,
        )
        async with async_db_session.begin() as db:
            db.add(user_obj)
        log.info(f"普通用户创建成功，账号：{username}，密码：{password}")

    async def fake_no_active_user(self):
        """ 自动创建锁定普通用户 """
        username = self.fake.user_name()
        password = self.fake.password()
        email = self.fake.email()
        user_obj = User(
            username=username,
            password=get_hash_password(password),
            email=email,
            is_active=False,
            is_superuser=False,
        )
        async with async_db_session.begin() as db:
            db.add(user_obj)
        log.info(f"普通锁定用户创建成功，账号：{username}，密码：{password}")

    async def fake_superuser(self):
        """ 自动创建管理员用户 """
        username = self.fake.user_name()
        password = self.fake.password()
        email = self.fake.email()
        user_obj = User(
            username=username,
            password=get_hash_password(password),
            email=email,
            is_superuser=True,
        )
        async with async_db_session.begin() as db:
            db.add(user_obj)
        log.info(f"管理员用户创建成功，账号：{username}，密码：{password}")

    async def fake_no_active_superuser(self):
        """ 自动创建锁定管理员用户 """
        username = self.fake.user_name()
        password = self.fake.password()
        email = self.fake.email()
        user_obj = User(
            username=username,
            password=get_hash_password(password),
            email=email,
            is_active=False,
            is_superuser=True,
        )
        async with async_db_session.begin() as db:
            db.add(user_obj)
        log.info(f"管理员锁定用户创建成功，账号：{username}，密码：{password}")

    async def init_data(self):
        """ 自动创建数据 """
        log.info('⏳ 开始初始化数据')
        await self.create_superuser_by_yourself()
        await self.fake_user()
        await self.fake_no_active_user()
        await self.fake_superuser()
        await self.fake_no_active_superuser()
        log.info('✅ 数据初始化完成')


if __name__ == '__main__':
    init = InitData()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init.init_data())
