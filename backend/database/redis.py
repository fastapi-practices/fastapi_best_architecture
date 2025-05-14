#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

from redis.asyncio import Redis
from redis.exceptions import AuthenticationError, TimeoutError

from backend.common.log import log
from backend.core.conf import settings


class RedisCli(Redis):
    """Redis client"""

    def __init__(self) -> None:
        """Initialize the Redis client"""
        super(RedisCli, self).__init__(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            db=settings.REDIS_DATABASE,
            socket_timeout=settings.REDIS_TIMEOUT,
            socket_connect_timeout=5,  # Connection timed out
            socket_keepalive=True,  # Keep Connection
            health_check_interval=30,  # Health checkup interval
            decode_responses=True,  # Transcode utf-8
            retry_on_timeout=True,  # Try overtime
            max_connections=20,  # Maximum number of connections
        )

    async def open(self) -> None:
        """Trigger Initialisation Connection"""
        try:
            await self.ping()
        except TimeoutError:
            log.error('❌ database retis connection timed out')
            sys.exit()
        except AuthenticationError:
            log.error('❌ database retis connection authentication failed')
            sys.exit()
        except Exception as e:
            log.error('❌database redis connection abnormal', e)
            sys.exit()

    async def delete_prefix(self, prefix: str, exclude: str | list[str] | None = None) -> None:
        """
        Remove all specified prefixes key

        :param prefix: prefix
        :param example: excluded key
        :return:
        """
        keys = []
        async for key in self.scan_iter(match=f'{prefix}*'):
            if isinstance(exclude, str):
                if key != exclude:
                    keys.append(key)
            elif isinstance(exclude, list):
                if key not in exclude:
                    keys.append(key)
            else:
                keys.append(key)
        if keys:
            await self.delete(*keys)


# create a single example of a redis client
redis_client: RedisCli = RedisCli()
