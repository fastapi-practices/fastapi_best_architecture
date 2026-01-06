import asyncio

from asyncio import Queue

from backend.common.log import log


async def batch_dequeue(queue: Queue, max_items: int, timeout: float) -> list:
    """
    从异步队列中获取多个项目

    :param queue: 用于获取项目的 `asyncio.Queue` 队列
    :param max_items: 从队列中获取的最大项目数量
    :param timeout: 总的等待超时时间（秒）
    :return:
    """
    items = []

    async def collector() -> None:
        while len(items) < max_items:
            item = await queue.get()
            items.append(item)

    try:
        await asyncio.wait_for(collector(), timeout=timeout)
    except asyncio.TimeoutError:
        pass
    except Exception as e:
        log.error(f'队列批量获取失败: {e}')

    return items
