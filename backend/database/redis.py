import sys

from redis.asyncio import Redis
from redis.exceptions import AuthenticationError, TimeoutError

from backend.common.log import log
from backend.core.conf import settings


class RedisCli(Redis):
    """Redis 客户端"""

    def __init__(self) -> None:
        """初始化 Redis 客户端"""
        super().__init__(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            db=settings.REDIS_DATABASE,
            socket_timeout=settings.REDIS_TIMEOUT,
            socket_connect_timeout=settings.REDIS_TIMEOUT,
            socket_keepalive=True,  # 保持连接
            health_check_interval=30,  # 健康检查间隔
            decode_responses=True,  # 转码 utf-8
        )

    async def open(self) -> None:
        """触发初始化连接"""
        try:
            await self.ping()
        except TimeoutError:
            log.error('❌ 数据库 redis 连接超时')
            sys.exit()
        except AuthenticationError:
            log.error('❌ 数据库 redis 连接认证失败')
            sys.exit()
        except Exception as e:
            log.error('❌ 数据库 redis 连接异常 {}', e)
            sys.exit()

    async def delete_prefix(self, prefix: str, exclude: str | list[str] | None = None, batch_size: int = 1000) -> None:
        """
        删除指定前缀的所有 key

        :param prefix: 要删除的键前缀
        :param exclude: 要排除的键或键列表
        :param batch_size: 批量删除的大小，避免一次性删除过多键导致 Redis 阻塞
        :return:
        """
        exclude_set = set(exclude) if isinstance(exclude, list) else {exclude} if isinstance(exclude, str) else set()
        batch_keys = []

        async for key in self.scan_iter(match=f'{prefix}*'):
            if key not in exclude_set:
                batch_keys.append(key)

                if len(batch_keys) >= batch_size:
                    await self.delete(*batch_keys)
                    batch_keys.clear()

        if batch_keys:
            await self.delete(*batch_keys)

    async def get_prefix(self, prefix: str, count: int = 100) -> list[str]:
        """
        获取指定前缀的所有 key

        :param prefix: 要搜索的键前缀
        :param count: 每次扫描批次的数量，值越大扫描速度越快，但会占用更多服务器资源
        :return:
        """
        return [key async for key in self.scan_iter(match=f'{prefix}*', count=count)]


# 创建 redis 客户端单例
redis_client: RedisCli = RedisCli()
