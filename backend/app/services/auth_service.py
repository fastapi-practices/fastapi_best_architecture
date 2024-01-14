#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from datetime import datetime

from fastapi import Request
from fastapi.security import OAuth2PasswordRequestForm
from starlette.background import BackgroundTasks

from backend.app.models import User
from backend.app.schemas.user import AuthLogin


class AuthServiceABC(ABC):
    """
    认证服务基类
    """

    @abstractmethod
    async def swagger_login(self, *, form_data: OAuth2PasswordRequestForm) -> tuple[str, User]:
        """
        Swagger表单登录

        :param form_data:
        :return:
        """
        pass

    @abstractmethod
    async def login(
        self, *, request: Request, obj: AuthLogin, background_tasks: BackgroundTasks
    ) -> tuple[str, str, datetime, datetime, User]:
        """
        用户登录

        :param request:
        :param obj:
        :param background_tasks:
        :return:
        """
        pass

    @abstractmethod
    async def new_token(self, *, request: Request, refresh_token: str) -> tuple[str, str, datetime, datetime]:
        """
        创建新Token

        :param request:
        :param refresh_token:
        :return:
        """
        pass

    @abstractmethod
    async def logout(self, *, request: Request) -> None:
        """
        用户登出

        :param request:
        :return:
        """
        pass
