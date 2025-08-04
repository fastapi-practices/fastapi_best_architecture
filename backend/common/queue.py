#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio

from asyncio import Queue
from typing import List

# 操作日志队列
opera_log_queue: Queue = Queue()


async def get_many_from_queue(queue: Queue, max_items: int, timeout: float) -> List:
    """
    在指定的超时时间内，从异步队列中批量获取项目。

    此函数会尝试从给定的 `asyncio.Queue` 中获取最多 `max_items` 个项目。
    它会为整个获取过程设置一个总的 `timeout` 秒数的超时限制。如果在超时
    时间内未能收集到 `max_items` 个项目，函数将返回当前已成功获取的所有项目。

    Args:
        queue: 用于获取项目的 `asyncio.Queue` 队列。
        max_items: 希望从队列中获取的最大项目数量。
        timeout: 总的等待超时时间（秒）。

    Returns:
        一个从队列中获取到的项目列表。如果发生超时，
        列表中的项目数量可能会少于 `max_items`。
    """
    results = []
    try:
        # 设置一个总的超时范围
        async with asyncio.timeout(timeout):
            while len(results) < max_items:
                item = await queue.get()
                results.append(item)
    except asyncio.TimeoutError:
        pass  # 超时后返回已有的 items
    return results
