import asyncio
import os
import time

from dataclasses import dataclass

from backend.common.dataclasses import SnowflakeInfo
from backend.common.exception import errors
from backend.common.log import log
from backend.core.conf import settings
from backend.database.redis import RedisCli


@dataclass(frozen=True)
class SnowflakeConfig:
    """雪花算法配置类"""

    # 位分配
    WORKER_ID_BITS: int = 5
    DATACENTER_ID_BITS: int = 5
    SEQUENCE_BITS: int = 12

    # 最大值
    MAX_WORKER_ID: int = (1 << WORKER_ID_BITS) - 1  # 31
    MAX_DATACENTER_ID: int = (1 << DATACENTER_ID_BITS) - 1  # 31
    SEQUENCE_MASK: int = (1 << SEQUENCE_BITS) - 1  # 4095

    # 位移偏移
    WORKER_ID_SHIFT: int = SEQUENCE_BITS
    DATACENTER_ID_SHIFT: int = SEQUENCE_BITS + WORKER_ID_BITS
    TIMESTAMP_LEFT_SHIFT: int = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS

    # 元年时间戳
    EPOCH: int = 1262275200000

    # 默认值
    DEFAULT_DATACENTER_ID: int = 1
    DEFAULT_WORKER_ID: int = 0
    DEFAULT_SEQUENCE: int = 0


class SnowflakeNodeManager:
    """雪花算法节点管理器，负责从 Redis 分配和管理节点 ID"""

    def __init__(self, redis_client: RedisCli) -> None:
        """
        初始化节点管理器

        :param redis_client: Redis 客户端实例
        """
        self.redis_client = redis_client
        self.prefix = settings.SNOWFLAKE_REDIS_PREFIX
        self.cluster_id: int | None = None
        self.node_id: int | None = None
        self.heartbeat_task: asyncio.Task | None = None

    async def acquire_node_id(self) -> tuple[int, int]:
        """
        从 Redis 获取可用的 cluster_id 和 node_id

        :return: (cluster_id, node_id)
        """
        # 查找所有已占用的节点
        occupied_nodes = set()
        pattern = f'{self.prefix}:nodes:*'
        async for key in self.redis_client.scan_iter(match=pattern):
            # 解析 key: {prefix}:nodes:{cluster_id}:{node_id}
            parts = key.split(':')
            if len(parts) >= 5:
                try:
                    cluster_id = int(parts[-2])
                    node_id = int(parts[-1])
                    occupied_nodes.add((cluster_id, node_id))
                except ValueError:
                    continue

        # 查找最小可用的 ID 组合
        for cluster_id in range(SnowflakeConfig.MAX_DATACENTER_ID + 1):
            for node_id in range(SnowflakeConfig.MAX_WORKER_ID + 1):
                # 尝试注册这个节点
                if (cluster_id, node_id) not in occupied_nodes and await self.register_node(cluster_id, node_id):
                    return cluster_id, node_id

        raise errors.ServerError(msg='无可用的雪花算法节点 ID，所有 ID 已被占用')

    async def register_node(self, cluster_id: int, node_id: int) -> bool:
        """
        注册节点并设置 TTL

        :param cluster_id: 集群 ID
        :param node_id: 节点 ID
        :return: 注册成功返回 True，失败返回 False
        """
        key = f'{self.prefix}:nodes:{cluster_id}:{node_id}'
        # 使用 SETNX 原子操作，只有 key 不存在时才设置
        # 存储进程信息用于调试
        value = f'pid:{os.getpid()}'
        success = await self.redis_client.set(key, value, nx=True, ex=settings.SNOWFLAKE_NODE_TTL)
        return bool(success)

    async def release_node(self, cluster_id: int, node_id: int) -> None:
        """
        释放节点 ID

        :param cluster_id: 集群 ID
        :param node_id: 节点 ID
        """
        key = f'{self.prefix}:nodes:{cluster_id}:{node_id}'
        await self.redis_client.delete(key)

    async def heartbeat(self, cluster_id: int, node_id: int) -> None:
        """
        心跳续期任务

        :param cluster_id: 集群 ID
        :param node_id: 节点 ID
        """
        key = f'{self.prefix}:nodes:{cluster_id}:{node_id}'
        try:
            while True:
                await asyncio.sleep(settings.SNOWFLAKE_HEARTBEAT_INTERVAL)
                try:
                    # 续期 TTL
                    await self.redis_client.expire(key, settings.SNOWFLAKE_NODE_TTL)
                    log.debug(f'雪花算法节点心跳: cluster_id={cluster_id}, node_id={node_id}')
                except Exception as e:
                    log.error(f'雪花算法节点心跳失败: {e}')
        except asyncio.CancelledError:
            log.info(f'雪花算法节点心跳任务取消: cluster_id={cluster_id}, node_id={node_id}')

    async def start_heartbeat(self, cluster_id: int, node_id: int) -> None:
        """
        启动心跳任务

        :param cluster_id: 集群 ID
        :param node_id: 节点 ID
        """
        self.cluster_id = cluster_id
        self.node_id = node_id
        self.heartbeat_task = asyncio.create_task(self.heartbeat(cluster_id, node_id))

    async def stop_heartbeat(self) -> None:
        """停止心跳任务"""
        if self.heartbeat_task:
            self.heartbeat_task.cancel()
            try:
                await self.heartbeat_task
            except asyncio.CancelledError:
                pass
            self.heartbeat_task = None


class Snowflake:
    """雪花算法类"""

    def __init__(
        self,
        cluster_id: int | None = None,
        node_id: int | None = None,
        sequence: int = SnowflakeConfig.DEFAULT_SEQUENCE,
    ) -> None:
        """
        初始化雪花算法生成器

        :param cluster_id: 集群 ID (0-31)，None 表示自动分配
        :param node_id: 节点 ID (0-31)，None 表示自动分配
        :param sequence: 起始序列号
        """
        self.node_id = node_id
        self.cluster_id = cluster_id
        self.sequence = sequence
        self.last_timestamp = -1
        self.node_manager: SnowflakeNodeManager | None = None
        self._initialized = False
        self._auto_allocated = False  # 标记是否是自动分配的 ID

    async def initialize(self) -> None:
        """
        初始化雪花算法，从环境变量或 Redis 获取节点 ID
        """
        if self._initialized:
            return

        # 优先从环境变量读取配置
        env_cluster_id = settings.SNOWFLAKE_CLUSTER_ID
        env_node_id = settings.SNOWFLAKE_NODE_ID

        if env_cluster_id is not None and env_node_id is not None:
            # 使用环境变量配置
            self.cluster_id = env_cluster_id
            self.node_id = env_node_id
            log.info(f'✅ 雪花算法使用环境变量配置: cluster_id={self.cluster_id}, node_id={self.node_id}')
        elif self.cluster_id is not None and self.node_id is not None:
            # 使用初始化时传入的配置
            log.info(f'✅ 雪花算法使用手动配置: cluster_id={self.cluster_id}, node_id={self.node_id}')
        else:
            # 从 Redis 自动分配
            from backend.database.redis import redis_client

            self.node_manager = SnowflakeNodeManager(redis_client)
            self.cluster_id, self.node_id = await self.node_manager.acquire_node_id()
            self._auto_allocated = True
            log.info(
                f'✅ 雪花算法从 Redis 自动分配: cluster_id={self.cluster_id}, node_id={self.node_id}, pid={os.getpid()}'
            )

            # 启动心跳任务
            await self.node_manager.start_heartbeat(self.cluster_id, self.node_id)

        # 验证 ID 范围
        if self.cluster_id < 0 or self.cluster_id > SnowflakeConfig.MAX_DATACENTER_ID:
            raise errors.RequestError(msg=f'集群编号必须在 0-{SnowflakeConfig.MAX_DATACENTER_ID} 之间')
        if self.node_id < 0 or self.node_id > SnowflakeConfig.MAX_WORKER_ID:
            raise errors.RequestError(msg=f'节点编号必须在 0-{SnowflakeConfig.MAX_WORKER_ID} 之间')

        self._initialized = True

    async def shutdown(self) -> None:
        """
        关闭雪花算法，释放节点 ID
        """
        if not self._initialized:
            return

        if self.node_manager and self._auto_allocated:
            # 停止心跳
            await self.node_manager.stop_heartbeat()

            # 释放节点
            if self.cluster_id is not None and self.node_id is not None:
                await self.node_manager.release_node(self.cluster_id, self.node_id)
                log.info(f'✅ 雪花算法节点已释放: cluster_id={self.cluster_id}, node_id={self.node_id}')

        self._initialized = False

    @staticmethod
    def _current_millis() -> int:
        """返回当前毫秒时间戳"""
        return int(time.time() * 1000)

    def _next_millis(self, last_timestamp: int) -> int:
        """
        等待至下一毫秒

        :param last_timestamp: 上次生成 ID 的时间戳
        :return:
        """
        timestamp = self._current_millis()
        while timestamp <= last_timestamp:
            time.sleep((last_timestamp - timestamp + 1) / 1000.0)
            timestamp = self._current_millis()
        return timestamp

    def generate(self) -> int:
        """生成雪花 ID"""
        if not self._initialized:
            raise errors.ServerError(msg='雪花算法未初始化，请先调用 initialize() 方法')

        if self.cluster_id is None or self.node_id is None:
            raise errors.ServerError(msg='雪花算法节点 ID 未设置')

        timestamp = self._current_millis()

        if timestamp < self.last_timestamp:
            raise errors.ServerError(msg=f'系统时间倒退，拒绝生成 ID 直到 {self.last_timestamp}')

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & SnowflakeConfig.SEQUENCE_MASK
            if self.sequence == 0:
                timestamp = self._next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        return (
            ((timestamp - SnowflakeConfig.EPOCH) << SnowflakeConfig.TIMESTAMP_LEFT_SHIFT)
            | (self.cluster_id << SnowflakeConfig.DATACENTER_ID_SHIFT)
            | (self.node_id << SnowflakeConfig.WORKER_ID_SHIFT)
            | self.sequence
        )

    @staticmethod
    def parse_id(snowflake_id: int) -> SnowflakeInfo:
        """
        解析雪花 ID，获取其包含的详细信息

        :param snowflake_id: 雪花ID
        :return:
        """
        timestamp = (snowflake_id >> SnowflakeConfig.TIMESTAMP_LEFT_SHIFT) + SnowflakeConfig.EPOCH
        cluster_id = (snowflake_id >> SnowflakeConfig.DATACENTER_ID_SHIFT) & SnowflakeConfig.MAX_DATACENTER_ID
        node_id = (snowflake_id >> SnowflakeConfig.WORKER_ID_SHIFT) & SnowflakeConfig.MAX_WORKER_ID
        sequence = snowflake_id & SnowflakeConfig.SEQUENCE_MASK

        return SnowflakeInfo(
            timestamp=timestamp,
            datetime=time.strftime(settings.DATETIME_FORMAT, time.localtime(timestamp / 1000)),
            cluster_id=cluster_id,
            node_id=node_id,
            sequence=sequence,
        )


snowflake = Snowflake()
