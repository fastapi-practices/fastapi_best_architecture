import asyncio

from asyncio import Queue
from time import perf_counter

from backend.common.log import log
from backend.common.observability.prometheus_queue import (
    observe_batch_dequeue_cost,
    observe_queue_exception,
    observe_queue_size,
)


async def batch_dequeue(queue: Queue, max_items: int, timeout: float, *, queue_name: str = 'default') -> list:
    """
    从异步队列中获取多个项目

    :param queue: 用于获取项目的 `asyncio.Queue` 队列
    :param max_items: 从队列中获取的最大项目数量
    :param timeout: 总的等待超时时间（秒）
    :param queue_name: 队列名称，用于 Prometheus 标签
    :return:
    """
    items = []
    start = perf_counter()

    async def collector() -> None:
        while len(items) < max_items:
            item = await queue.get()
            items.append(item)
            observe_queue_size(queue, queue_name=queue_name)

    try:
        await asyncio.wait_for(collector(), timeout=timeout)
    except asyncio.TimeoutError:
        pass
    except Exception as e:
        observe_queue_exception(queue_name=queue_name)
        log.error(f'队列批量获取失败: {e}')
    finally:
        observe_batch_dequeue_cost(start, queue_name=queue_name)
        observe_queue_size(queue, queue_name=queue_name)

    return items
