import asyncio
import atexit
import threading
import weakref

from functools import wraps
from typing import Any, Awaitable, Callable, Coroutine, TypeVar

T = TypeVar('T')


class _TaskRunner:
    """在后台线程上运行 asyncio 事件循环的任务运行器"""

    def __init__(self):
        self.__loop: asyncio.AbstractEventLoop | None = None
        self.__thread: threading.Thread | None = None
        self.__lock = threading.Lock()
        atexit.register(self.close)

    def close(self):
        """关闭事件循环并清理"""
        if self.__loop:
            self.__loop.stop()
            self.__loop = None
        if self.__thread:
            self.__thread.join()
            self.__thread = None
        name = f'TaskRunner-{threading.get_ident()}'
        _runner_map.pop(name, None)

    def _target(self):
        """后台线程的目标函数"""
        try:
            self.__loop.run_forever()
        finally:
            self.__loop.close()

    def run(self, coro: Awaitable[T]) -> T:
        """在后台事件循环上运行协程并返回其结果"""
        with self.__lock:
            name = f'TaskRunner-{threading.get_ident()}'
            if self.__loop is None:
                self.__loop = asyncio.new_event_loop()
                self.__thread = threading.Thread(target=self._target, daemon=True, name=name)
                self.__thread.start()
            future = asyncio.run_coroutine_threadsafe(coro, self.__loop)
            return future.result()


_runner_map = weakref.WeakValueDictionary()


def run_await(coro: Callable[..., Awaitable[T]] | Callable[..., Coroutine[Any, Any, T]]) -> Callable[..., T]:
    """将协程包装在函数中，该函数将在后台事件循环上运行，直到它执行完为止"""

    @wraps(coro)
    def wrapped(*args, **kwargs):
        inner = coro(*args, **kwargs)
        if not asyncio.iscoroutine(inner) and not asyncio.isfuture(inner):
            raise TypeError(f'Expected coroutine, got {type(inner)}')
        try:
            # 如果事件循环正在运行，则使用任务调用
            asyncio.get_running_loop()
            name = f'TaskRunner-{threading.get_ident()}'
            if name not in _runner_map:
                _runner_map[name] = _TaskRunner()
            return _runner_map[name].run(inner)
        except RuntimeError:
            # 如果没有，则创建一个新的事件循环
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(inner)

    wrapped.__doc__ = coro.__doc__
    return wrapped
