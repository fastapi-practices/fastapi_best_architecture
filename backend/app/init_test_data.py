#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio

from email_validator import EmailNotValidError, validate_email
from faker import Faker

from backend.app.common.jwt import get_hash_password
from backend.app.common.log import log
from backend.app.database.db_mysql import async_db_session
from backend.app.models import User, Role, Menu, Dept


class InitTestData:
    """初始化测试数据"""

    def __init__(self, session):
        self.fake = Faker('zh_CN')
        self.session = session

    async def create_dept(self):
        """自动创建部门"""
        async with self.session.begin() as db:
            department_obj = Dept(name='test', create_user=1)
            db.add(department_obj)
        log.info('部门 test 创建成功')

    async def create_role(self):
        """自动创建角色"""
        async with self.session.begin() as db:
            role_obj = Role(name='test', create_user=1)
            role_obj.menus.append(Menu(name='test', create_user=1))
            db.add(role_obj)
        log.info('角色 test 创建成功')

    async def create_test_user(self):
        """创建测试用户"""
        username = 'test'
        password = 'test'
        email = 'test@gmail.com'
        user_obj = User(
            username=username,
            nickname=username,
            password=get_hash_password(password),
            email=email,
            is_superuser=True,
            dept_id=1,
        )
        async with self.session.begin() as db:
            user_obj.roles.append(await db.get(Role, 1))
            db.add(user_obj)
        log.info(f'测试用户创建成功，账号：{username}，密码：{password}')

    async def create_superuser_by_yourself(self):
        """手动创建管理员账户"""
        log.info('开始创建自定义管理员用户')
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
            nickname=username,
            password=get_hash_password(password),
            email=email,
            is_superuser=True,
            dept_id=1,
        )
        async with self.session.begin() as db:
            user_obj.roles.append(await db.get(Role, 1))
            db.add(user_obj)
        log.info(f'自定义管理员用户创建成功，账号：{username}，密码：{password}')

    async def fake_user(self):
        """自动创建普通用户"""
        username = self.fake.user_name()
        password = self.fake.password()
        email = self.fake.email()
        user_obj = User(
            username=username,
            nickname=username,
            password=get_hash_password(password),
            email=email,
            is_superuser=False,
            dept_id=1,
        )
        async with self.session.begin() as db:
            user_obj.roles.append(await db.get(Role, 1))
            db.add(user_obj)
        log.info(f'普通用户创建成功，账号：{username}，密码：{password}')

    async def fake_no_active_user(self):
        """自动创建锁定普通用户"""
        username = self.fake.user_name()
        password = self.fake.password()
        email = self.fake.email()
        user_obj = User(
            username=username,
            nickname=username,
            password=get_hash_password(password),
            email=email,
            is_active=False,
            is_superuser=False,
            dept_id=1,
        )
        async with self.session.begin() as db:
            user_obj.roles.append(await db.get(Role, 1))
            db.add(user_obj)
        log.info(f'普通锁定用户创建成功，账号：{username}，密码：{password}')

    async def fake_superuser(self):
        """自动创建管理员用户"""
        username = self.fake.user_name()
        password = self.fake.password()
        email = self.fake.email()
        user_obj = User(
            username=username,
            nickname=username,
            password=get_hash_password(password),
            email=email,
            is_superuser=True,
            dept_id=1,
        )
        async with self.session.begin() as db:
            user_obj.roles.append(await db.get(Role, 1))
            db.add(user_obj)
        log.info(f'管理员用户创建成功，账号：{username}，密码：{password}')

    async def fake_no_active_superuser(self):
        """自动创建锁定管理员用户"""
        username = self.fake.user_name()
        password = self.fake.password()
        email = self.fake.email()
        user_obj = User(
            username=username,
            nickname=username,
            password=get_hash_password(password),
            email=email,
            is_active=False,
            is_superuser=True,
            dept_id=1,
        )
        async with self.session.begin() as db:
            user_obj.roles.append(await db.get(Role, 1))
            db.add(user_obj)
        log.info(f'管理员锁定用户创建成功，账号：{username}，密码：{password}')

    async def init_data(self):
        """自动创建数据"""
        log.info('⏳ 开始初始化数据')
        await self.create_dept()
        await self.create_role()
        await self.create_test_user()
        await self.create_superuser_by_yourself()
        await self.fake_user()
        await self.fake_no_active_user()
        await self.fake_superuser()
        await self.fake_no_active_superuser()
        log.info('✅ 数据初始化完成')


if __name__ == '__main__':
    init = InitTestData(session=async_db_session)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init.init_data())
