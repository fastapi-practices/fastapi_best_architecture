#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import Request, Response
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.background import BackgroundTask, BackgroundTasks

from backend.app.admin.conf import admin_settings
from backend.app.admin.crud.crud_user import user_dao
import bcrypt
from backend.app.admin.model import User, Role
from backend.app.admin.schema.token import GetLoginToken, GetNewToken
from backend.app.admin.schema.user import AuthLoginParam, AddUserParam
from backend.common.security.jwt import get_hash_password
from backend.app.admin.service.login_log_service import login_log_service
from backend.common.enums import LoginLogStatusType
from backend.common.exception import errors
from backend.common.log import log
from backend.common.response.response_code import CustomErrorCode
from backend.common.security.jwt import (
    create_access_token,
    create_new_token,
    create_refresh_token,
    get_token,
    jwt_decode,
    password_verify,
)
from backend.core.conf import settings
from backend.database.db import async_db_session, uuid4_str
from backend.database.redis import redis_client
from backend.utils.timezone import timezone

from ldap3 import Server, Connection, ALL, SUBTREE, NTLM

class AuthService:
    """认证服务类"""

    @staticmethod
    async def user_verify(db: AsyncSession, username: str, password: str | None) -> User:
        """
        验证用户名和密码

        :param db: 数据库会话
        :param username: 用户名
        :param password: 密码
        :return:
        """
        user = await user_dao.get_by_username(db, username)
        if not user:
            raise errors.NotFoundError(msg='用户名或密码有误')

        if user.password is None:
            raise errors.AuthorizationError(msg='用户名或密码有误')
        else:
            if not password_verify(password, user.password):
                raise errors.AuthorizationError(msg='用户名或密码有误')

        if not user.status:
            raise errors.AuthorizationError(msg='用户已被锁定, 请联系统管理员')

        return user

    async def swagger_login(self, *, obj: HTTPBasicCredentials) -> tuple[str, User]:
        """
        Swagger 文档登录

        :param obj: 登录凭证
        :return:
        """
        async with async_db_session.begin() as db:
            user = await self.user_verify(db, obj.username, obj.password)
            await user_dao.update_login_time(db, obj.username)
            a_token = await create_access_token(
                str(user.id),
                user.is_multi_login,
                # extra info
                swagger=True,
            )
            return a_token.access_token, user

    async def swagger_ldap_login(self, *, obj: HTTPBasicCredentials) -> tuple[str, User]:
        """
        Swagger 文档LDAP登录

        :param obj: 登录凭证
        :return:
        """
        # 先进行LDAP认证
        ldap_result = await self.ldap_verify(obj.username, obj.password)
        if not ldap_result[0]:
            raise errors.AuthorizationError(msg=ldap_result[4])

        # 确保LDAP用户存在且有效
        if not ldap_result[2]:  # 检查sAMAccountName是否存在
            raise errors.AuthorizationError(msg="LDAP用户信息不完整")

        # 在同一个会话中处理所有数据库操作
        async with async_db_session.begin() as db:
            # 检查用户是否存在
            user = await user_dao.get_by_username(db, obj.username)

            # 如果用户不存在，创建新用户
            if not user:
                log.info(f"Creating new user from LDAP: {obj.username}")
                # 准备用户数据
                nickname = ldap_result[3] or obj.username
                email = ldap_result[1] or f"{obj.username}@wilmar.cn"

                # 检查昵称和邮箱是否已存在
                unique_nickname = nickname
                unique_email = email

                nickname_check = await user_dao.get_by_nickname(db, nickname)
                if nickname_check:
                    import random
                    unique_nickname = f"#{random.randrange(10000, 88888)}"

                email_check = await user_dao.check_email(db, email)
                if email_check:
                    import random
                    unique_email = f"{obj.username}_{random.randrange(1000, 9999)}@wilmar.cn"

                # 创建用户数据对象
                register_param = AddUserParam(
                    username=obj.username,
                    nickname=unique_nickname,
                    password="password",  # 需要提供一个非空密码，会被加密后存储
                    email=unique_email,
                    dept_id=1,  # 设置默认部门ID
                    roles=[1],  # 设置默认角色ID列表
                    status=1  # 设置用户状态为启用
                )

                try:
                    # 创建用户
                    salt = bcrypt.gensalt()
                    hashed_password = get_hash_password("password", salt)

                    # 直接使用模型创建用户，避免使用add方法
                    new_user = User(
                        username=obj.username,
                        nickname=unique_nickname,
                        password=hashed_password,
                        email=unique_email,
                        dept_id=1,
                        status=1,
                        is_staff=True,
                        salt=salt
                    )

                    # 添加角色
                    role = await db.get(Role, 1)
                    if role:
                        new_user.roles.append(role)

                    # 添加到数据库
                    db.add(new_user)
                    await db.flush()  # 确保用户被写入数据库

                    log.info(f"Successfully created user: {obj.username} with ID: {new_user.id}")

                    # 使用创建的用户对象
                    user = new_user
                except Exception as e:
                    error_msg = f'用户创建失败，请联系管理员: {str(e) if str(e) else "数据库错误"}'
                    log.error(f"Error creating user: {error_msg}", exc_info=True)
                    raise errors.AuthorizationError(msg=error_msg)

            # 检查用户状态
            if not user.status:
                raise errors.AuthorizationError(msg='用户已被锁定，请联系管理员')

            # 更新登录时间
            await user_dao.update_login_time(db, obj.username)
            await db.refresh(user)

            # 创建访问令牌
            a_token = await create_access_token(
                str(user.id),
                user.is_multi_login,
                # extra info
                swagger=True,
            )
            return a_token.access_token, user



    async def login(
        self, *, request: Request, response: Response, obj: AuthLoginParam, background_tasks: BackgroundTasks
    ) -> GetLoginToken:
        """
        用户登录

        :param request: 请求对象
        :param response: 响应对象
        :param obj: 登录参数
        :param background_tasks: 后台任务
        :return:
        """
        async with async_db_session.begin() as db:
            user = None
            try:
                user = await self.user_verify(db, obj.username, obj.password)
                captcha_code = await redis_client.get(f'{admin_settings.CAPTCHA_LOGIN_REDIS_PREFIX}:{request.state.ip}')
                if not captcha_code:
                    raise errors.AuthorizationError(msg='验证码失效，请重新获取')
                if captcha_code.lower() != obj.captcha.lower():
                    raise errors.CustomError(error=CustomErrorCode.CAPTCHA_ERROR)
                await redis_client.delete(f'{admin_settings.CAPTCHA_LOGIN_REDIS_PREFIX}:{request.state.ip}')
                await user_dao.update_login_time(db, obj.username)
                await db.refresh(user)
                a_token = await create_access_token(
                    str(user.id),
                    user.is_multi_login,
                    # extra info
                    username=user.username,
                    nickname=user.nickname,
                    last_login_time=timezone.t_str(user.last_login_time),
                    ip=request.state.ip,
                    os=request.state.os,
                    browser=request.state.browser,
                    device=request.state.device,
                )
                r_token = await create_refresh_token(str(user.id), user.is_multi_login)
                response.set_cookie(
                    key=settings.COOKIE_REFRESH_TOKEN_KEY,
                    value=r_token.refresh_token,
                    max_age=settings.COOKIE_REFRESH_TOKEN_EXPIRE_SECONDS,
                    expires=timezone.f_utc(r_token.refresh_token_expire_time),
                    httponly=True,
                )
            except errors.NotFoundError as e:
                log.error('登陆错误: 用户名不存在')
                raise errors.NotFoundError(msg=e.msg)
            except (errors.AuthorizationError, errors.CustomError) as e:
                if not user:
                    log.error('登陆错误: 用户密码有误')
                task = BackgroundTask(
                    login_log_service.create,
                    **dict(
                        db=db,
                        request=request,
                        user_uuid=user.uuid if user else uuid4_str(),
                        username=obj.username,
                        login_time=timezone.now(),
                        status=LoginLogStatusType.fail.value,
                        msg=e.msg,
                    ),
                )
                raise errors.AuthorizationError(msg=e.msg, background=task)
            except Exception as e:
                log.error(f'登陆错误: {e}')
                raise e
            else:
                background_tasks.add_task(
                    login_log_service.create,
                    **dict(
                        db=db,
                        request=request,
                        user_uuid=user.uuid,
                        username=obj.username,
                        login_time=timezone.now(),
                        status=LoginLogStatusType.success.value,
                        msg='登录成功',
                    ),
                )
                data = GetLoginToken(
                    access_token=a_token.access_token,
                    access_token_expire_time=a_token.access_token_expire_time,
                    session_uuid=a_token.session_uuid,
                    user=user,  # type: ignore
                )
                return data

    @staticmethod
    async def new_token(*, request: Request) -> GetNewToken:
        """
        获取新的访问令牌

        :param request: FastAPI 请求对象
        :return:
        """
        refresh_token = request.cookies.get(settings.COOKIE_REFRESH_TOKEN_KEY)
        if not refresh_token:
            raise errors.TokenError(msg='Refresh Token 已过期，请重新登录')
        try:
            user_id = jwt_decode(refresh_token).id
        except Exception:
            raise errors.TokenError(msg='Refresh Token 无效')
        async with async_db_session() as db:
            user = await user_dao.get(db, user_id)
            if not user:
                raise errors.NotFoundError(msg='用户名或密码有误')
            elif not user.status:
                raise errors.AuthorizationError(msg='用户已被锁定, 请联系统管理员')
            new_token = await create_new_token(
                user_id=str(user.id),
                refresh_token=refresh_token,
                multi_login=user.is_multi_login,
                # extra info
                username=user.username,
                nickname=user.nickname,
                last_login_time=timezone.t_str(user.last_login_time),
                ip=request.state.ip,
                os=request.state.os,
                browser=request.state.browser,
                device_type=request.state.device,
            )
            data = GetNewToken(
                access_token=new_token.new_access_token,
                access_token_expire_time=new_token.new_access_token_expire_time,
                session_uuid=new_token.session_uuid,
            )
            return data

    @staticmethod
    async def ldap_user_verify(username: str, password: str) -> User:
        """
        验证用户名和密码

        :param username: 用户名
        :param password: 密码
        :return:
        """
        # 先进行LDAP认证
        try:
            # 1. LDAP认证
            ldap_result = await AuthService.ldap_verify(username, password)
            log.info(f"LDAP verification result: {ldap_result}")

            if not ldap_result[0]:  # LDAP认证失败
                raise errors.AuthorizationError(msg=ldap_result[4])  # 使用具体的错误信息

            # 2. 检查用户是否存在
            user = None
            db = None

            try:
                db = async_db_session()
                user = await user_dao.get_by_username(db, username)
            finally:
                if db:
                    await db.close()

            # 3. 如果用户不存在，创建新用户
            if not user:
                # 准备用户数据
                nickname = ldap_result[3] or username
                email = ldap_result[1] or f"{username}@{admin_settings.LDAP_BASE_DC}.cn"

                # 检查昵称和邮箱是否已存在
                unique_nickname = nickname
                unique_email = email

                try:
                    db = async_db_session()
                    nickname_check = await user_dao.get_by_nickname(db, nickname)
                    if nickname_check:
                        import random
                        unique_nickname = f"#{random.randrange(10000, 88888)}"

                    email_check = await user_dao.check_email(db, email)
                    if email_check:
                        import random
                        unique_email = f"{username}_{random.randrange(1000, 9999)}@{admin_settings.LDAP_BASE_DC}.cn"
                finally:
                    if db:
                        await db.close()

                # 创建用户数据对象
                register_param = AddUserParam(
                    username=username,
                    nickname=unique_nickname,
                    password="",  # 不保存密码
                    email=unique_email,
                    dept_id=1,  # 设置默认部门ID
                    roles=[1],  # 设置默认角色ID列表
                    status=1  # 设置用户状态为启用
                )

                # 创建用户
                try:
                    log.info(f"Creating new user: {username}")
                    db = async_db_session()
                    await db.begin()
                    # 使用 add 方法替代 create 方法
                    await user_dao.add(db, register_param)
                    await db.commit()
                    # 获取新创建的用户
                    user = await user_dao.get_by_username(db, username)
                    log.info(f"Created new user: {username}")
                except Exception as e:
                    if db:
                        await db.rollback()
                    log.error(f"Error creating user: {str(e)}", exc_info=True)
                    raise errors.AuthorizationError(msg=f'用户创建失败，请联系管理员: {str(e)}')
                finally:
                    if db:
                        await db.close()

            # 4. 检查用户状态
            if not user:
                raise errors.AuthorizationError(msg='用户不存在或创建失败')
            elif not user.status:
                raise errors.AuthorizationError(msg='用户已被锁定，请联系管理员')

            return user
        except errors.AuthorizationError:
            raise
        except Exception as e:
            log.error(f"Error during user verification: {str(e)}", exc_info=True)
            raise errors.AuthorizationError(msg=f'LDAP认证失败: {str(e)}')

    @staticmethod
    async def ldap_verify(username: str, password: str) -> tuple:
        try:
            # 配置LDAP服务器
            ldap_server = Server(
                host=admin_settings.LDAP_SERVER,
                port=admin_settings.LDAP_PORT,  # LDAPS端口
                use_ssl=True,
                get_info=ALL
            )

            # 创建连接并尝试绑定
            conn = Connection(
                ldap_server,
                user=f'{admin_settings.LDAP_BASE_DC}\\{username}',
                password=password,
                authentication=NTLM,
                auto_bind=True,
                raise_exceptions=False
            )

            if not conn.bound:
                log.warning(f"LDAP bind failed for user: {username}")
                return (False, None, None, None, "用户名或密码错误")

            log.info(f"LDAP connection established for user: {username}")

            # 搜索用户信息
            search_result = conn.search(
                search_base=admin_settings.LDAP_BASE_DN,
                search_filter=f'(sAMAccountName={username})',
                search_scope=SUBTREE,
                attributes=['cn', 'givenName', 'mail', 'sAMAccountName']
            )

            if not search_result or len(conn.response) == 0:
                log.warning(f"User not found in LDAP: {username}")
                return (False, None, None, None, "LDAP中未找到该用户")

            entry = conn.response[0]
            attr_dict = entry['attributes']

            log.info(f"Found user in LDAP: {entry['dn']}")

            # 返回成功结果
            return (True,
                   attr_dict.get("mail", ""),
                   attr_dict.get("sAMAccountName", ""),
                   attr_dict.get("givenName", ""),
                   "登录成功")

        except Exception as e:
            log.error(f"LDAP verification error: {str(e)}")
            return (False, None, None, None, f"LDAP连接失败: {str(e)}")

    async def ldap_login(
        self, *, request: Request, response: Response, obj: AuthLoginParam, background_tasks: BackgroundTasks
    ) -> GetLoginToken:
        """
        LDAP用户登录

        :param request: 请求对象
        :param response: 响应对象
        :param obj: 登录参数
        :param background_tasks: 后台任务
        :return:
        """
        async with async_db_session.begin() as db:
            user = None
            try:
                # 验证验证码
                captcha_code = await redis_client.get(f'{admin_settings.CAPTCHA_LOGIN_REDIS_PREFIX}:{request.state.ip}')
                if not captcha_code:
                    raise errors.AuthorizationError(msg='验证码失效，请重新获取')
                if captcha_code.lower() != obj.captcha.lower():
                    raise errors.CustomError(error=CustomErrorCode.CAPTCHA_ERROR)
                await redis_client.delete(f'{admin_settings.CAPTCHA_LOGIN_REDIS_PREFIX}:{request.state.ip}')

                # 使用LDAP验证用户
                user = await self.ldap_user_verify(obj.username, obj.password)

                # 更新登录时间
                await user_dao.update_login_time(db, obj.username)
                await db.refresh(user)

                # 创建访问令牌和刷新令牌
                a_token = await create_access_token(
                    str(user.id),
                    user.is_multi_login,
                    # extra info
                    username=user.username,
                    nickname=user.nickname,
                    last_login_time=timezone.t_str(user.last_login_time),
                    ip=request.state.ip,
                    os=request.state.os,
                    browser=request.state.browser,
                    device=request.state.device,
                )
                r_token = await create_refresh_token(str(user.id), user.is_multi_login)

                # 设置刷新令牌cookie
                response.set_cookie(
                    key=settings.COOKIE_REFRESH_TOKEN_KEY,
                    value=r_token.refresh_token,
                    max_age=settings.COOKIE_REFRESH_TOKEN_EXPIRE_SECONDS,
                    expires=timezone.f_utc(r_token.refresh_token_expire_time),
                    httponly=True,
                )
            except errors.NotFoundError as e:
                log.error('登陆错误: 用户名不存在')
                raise errors.NotFoundError(msg=e.msg)
            except (errors.AuthorizationError, errors.CustomError) as e:
                if not user:
                    log.error('登陆错误: 用户密码有误')
                task = BackgroundTask(
                    login_log_service.create,
                    **dict(
                        db=db,
                        request=request,
                        user_uuid=user.uuid if user else uuid4_str(),
                        username=obj.username,
                        login_time=timezone.now(),
                        status=LoginLogStatusType.fail.value,
                        msg=e.msg,
                    ),
                )
                raise errors.AuthorizationError(msg=e.msg, background=task)
            except Exception as e:
                log.error(f'登陆错误: {e}', exc_info=True)
                raise e
            else:
                background_tasks.add_task(
                    login_log_service.create,
                    **dict(
                        db=db,
                        request=request,
                        user_uuid=user.uuid,
                        username=obj.username,
                        login_time=timezone.now(),
                        status=LoginLogStatusType.success.value,
                        msg='登录成功',
                    ),
                )
                data = GetLoginToken(
                    access_token=a_token.access_token,
                    access_token_expire_time=a_token.access_token_expire_time,
                    session_uuid=a_token.session_uuid,
                    user=user,  # type: ignore
                )
                return data

    @staticmethod
    async def logout(*, request: Request, response: Response) -> None:
        """
        用户登出

        :param request: FastAPI 请求对象
        :param response: FastAPI 响应对象
        :return:
        """
        token = get_token(request)
        token_payload = jwt_decode(token)
        user_id = token_payload.id
        refresh_token = request.cookies.get(settings.COOKIE_REFRESH_TOKEN_KEY)
        response.delete_cookie(settings.COOKIE_REFRESH_TOKEN_KEY)
        if request.user.is_multi_login:
            await redis_client.delete(f'{settings.TOKEN_REDIS_PREFIX}:{user_id}:{token_payload.session_uuid}')
            if refresh_token:
                await redis_client.delete(f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{user_id}:{refresh_token}')
        else:
            key_prefix = [
                f'{settings.TOKEN_REDIS_PREFIX}:{user_id}:',
                f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{user_id}:',
            ]
            for prefix in key_prefix:
                await redis_client.delete_prefix(prefix)


auth_service: AuthService = AuthService()
