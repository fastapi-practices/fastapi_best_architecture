#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

from aioredis import Redis, TimeoutError, AuthenticationError

from backend.app.common.log import log
from backend.app.core.conf import settings


class RedisCli(Redis):

    def __init__(self):
        super(RedisCli, self).__init__(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            db=settings.REDIS_DATABASE,
            socket_timeout=settings.REDIS_TIMEOUT,
            decode_responses=True  # 转码 utf-8
        )

    async def open(self):
        """
        触发初始化连接

        :return:
        """
        try:
            await self.ping()
        except TimeoutError:
            log.error("❌ 数据库 redis 连接超时")
            sys.exit()
        except AuthenticationError:
            log.error("❌ 数据库 redis 连接认证失败")
            sys.exit()
        except Exception as e:
            log.error('❌ 数据库 redis 连接异常 {}', e)
            sys.exit()


# 创建redis连接对象
redis_client = RedisCli()
