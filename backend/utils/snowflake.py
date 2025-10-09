import time

from dataclasses import dataclass

from backend.common.dataclasses import SnowflakeInfo
from backend.common.exception import errors
from backend.core.conf import settings


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


class Snowflake:
    """雪花算法类"""

    def __init__(
        self,
        cluster_id: int = SnowflakeConfig.DEFAULT_DATACENTER_ID,
        node_id: int = SnowflakeConfig.DEFAULT_WORKER_ID,
        sequence: int = SnowflakeConfig.DEFAULT_SEQUENCE,
    ) -> None:
        """
        初始化雪花算法生成器

        :param cluster_id: 集群 ID (0-31)
        :param node_id: 节点 ID (0-31)
        :param sequence: 起始序列号
        """
        if cluster_id < 0 or cluster_id > SnowflakeConfig.MAX_DATACENTER_ID:
            raise errors.RequestError(msg=f'集群编号必须在 0-{SnowflakeConfig.MAX_DATACENTER_ID} 之间')
        if node_id < 0 or node_id > SnowflakeConfig.MAX_WORKER_ID:
            raise errors.RequestError(msg=f'节点编号必须在 0-{SnowflakeConfig.MAX_WORKER_ID} 之间')

        self.node_id = node_id
        self.cluster_id = cluster_id
        self.sequence = sequence
        self.last_timestamp = -1

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
