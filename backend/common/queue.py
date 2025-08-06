#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio

from asyncio import Queue


async def batch_dequeue(queue: Queue, max_items: int, timeout: float) -> list:
    """
    从异步队列中获取多个项目

    :param queue: 用于获取项目的 `asyncio.Queue` 队列
    :param max_items: 从队列中获取的最大项目数量
    :param timeout: 总的等待超时时间（秒）
    :return:
    """
    items = []

    loop = asyncio.get_event_loop()
    end_time = loop.time() + timeout

    while len(items) < max_items:
        remaining = end_time - loop.time()
        if remaining <= 0:
            break
        try:
            item = await asyncio.wait_for(queue.get(), timeout=remaining)
            items.append(item)
        except asyncio.TimeoutError:
            break

    return items
