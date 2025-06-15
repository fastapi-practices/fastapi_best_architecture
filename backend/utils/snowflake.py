#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Twitter雪花算法(Snowflake)的Python实现
用于生成分布式唯一ID

ID结构(64位):
- 1位符号位，固定为0
- 41位时间戳(毫秒级)
- 5位数据中心ID
- 5位机器ID
- 12位序列号

https://github.com/twitter-archive/snowflake/blob/snowflake-2010/src/main/scala/com/twitter/service/snowflake/IdWorker.scala
"""

import time

from dataclasses import dataclass


class SnowflakeException(Exception):
    """雪花算法基础异常类"""

    pass


class InvalidSystemClock(SnowflakeException):
    """时钟回拨异常"""

    pass


class InvalidWorkerId(SnowflakeException):
    """无效的工作节点ID异常"""

    pass


class InvalidDatacenterId(SnowflakeException):
    """无效的数据中心ID异常"""

    pass


@dataclass
class SnowflakeConfig:
    """雪花算法配置类"""

    # 64位ID的划分
    WORKER_ID_BITS: int = 5
    DATACENTER_ID_BITS: int = 5
    SEQUENCE_BITS: int = 12

    # 最大取值计算
    MAX_WORKER_ID: int = -1 ^ (-1 << WORKER_ID_BITS)  # 2**5-1 0b11111
    MAX_DATACENTER_ID: int = -1 ^ (-1 << DATACENTER_ID_BITS)

    # 移位偏移计算
    WORKER_ID_SHIFT: int = SEQUENCE_BITS
    DATACENTER_ID_SHIFT: int = SEQUENCE_BITS + WORKER_ID_BITS
    TIMESTAMP_LEFT_SHIFT: int = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS

    # 序号循环掩码
    SEQUENCE_MASK: int = -1 ^ (-1 << SEQUENCE_BITS)

    # 元年时间戳, 2010-01-01 00:00:00
    EPOCH: int = 1262275200000

    # 默认配置
    DEFAULT_DATACENTER_ID: int = 1
    DEFAULT_WORKER_ID: int = 0
    DEFAULT_SEQUENCE: int = 0


class Snowflake:
    """雪花算法ID生成器"""

    def __init__(
        self,
        datacenter_id: int = SnowflakeConfig.DEFAULT_DATACENTER_ID,
        worker_id: int = SnowflakeConfig.DEFAULT_WORKER_ID,
        sequence: int = SnowflakeConfig.DEFAULT_SEQUENCE,
    ):
        """
        初始化ID生成器

        :param datacenter_id: 数据中心ID (0-31)
        :param worker_id: 工作节点ID (0-31)
        :param sequence: 起始序列号
        """
        if not 0 <= worker_id <= SnowflakeConfig.MAX_WORKER_ID:
            raise InvalidWorkerId(f'工作节点ID必须在0-{SnowflakeConfig.MAX_WORKER_ID}之间')

        if not 0 <= datacenter_id <= SnowflakeConfig.MAX_DATACENTER_ID:
            raise InvalidDatacenterId(f'数据中心ID必须在0-{SnowflakeConfig.MAX_DATACENTER_ID}之间')

        self.worker_id = worker_id
        self.datacenter_id = datacenter_id
        self.sequence = sequence
        self.last_timestamp = -1

    def __call__(self) -> int:
        """使实例可调用，用于default_factory"""
        return self.generate()

    @staticmethod
    def _gen_timestamp() -> int:
        """
        生成当前时间戳，单位：毫秒

        :return: 当前时间戳
        """
        return int(time.time() * 1000)

    def _til_next_millis(self, last_timestamp: int) -> int:
        """
        等待到下一个毫秒

        :param last_timestamp: 上次生成ID的时间戳
        :return: 下一个毫秒的时间戳
        """
        timestamp = self._gen_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._gen_timestamp()
        return timestamp

    def generate(self) -> int:
        """
        获取新的唯一ID，单位：毫秒

        :return: 新的唯一ID
        """
        timestamp = self._gen_timestamp()

        if timestamp < self.last_timestamp:
            raise InvalidSystemClock(f'系统时钟回拨，拒绝生成ID直到 {self.last_timestamp}')

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & SnowflakeConfig.SEQUENCE_MASK
            if self.sequence == 0:
                timestamp = self._til_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        new_id = (
            ((timestamp - SnowflakeConfig.EPOCH) << SnowflakeConfig.TIMESTAMP_LEFT_SHIFT)
            | (self.datacenter_id << SnowflakeConfig.DATACENTER_ID_SHIFT)
            | (self.worker_id << SnowflakeConfig.WORKER_ID_SHIFT)
            | self.sequence
        )
        return new_id


snowflake = Snowflake()

if __name__ == '__main__':
    for _ in range(10):
        print(snowflake.generate())
