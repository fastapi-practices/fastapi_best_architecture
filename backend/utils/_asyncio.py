#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import atexit
import threading
import weakref

from typing import Awaitable, Callable, TypeVar

T = TypeVar('T')


class _TaskRunner:
    """A task runner that runs an asyncio event loop on a background thread."""

    def __init__(self):
        self.__loop: asyncio.AbstractEventLoop | None = None
        self.__thread: threading.Thread | None = None
        self.__lock = threading.Lock()
        atexit.register(self.close)

    def close(self):
        """关闭事件循环"""
        if self.__loop:
            self.__loop.stop()

    def _target(self):
        """后台线程目标"""
        loop = self.__loop
        try:
            loop.run_forever()
        finally:
            loop.close()

    def run(self, coro):
        """在后台线程上同步运行协程"""
        with self.__lock:
            name = f'{threading.current_thread().name} - runner'
            if self.__loop is None:
                self.__loop = asyncio.new_event_loop()
                self.__thread = threading.Thread(target=self._target, daemon=True, name=name)
                self.__thread.start()
        fut = asyncio.run_coroutine_threadsafe(coro, self.__loop)
        return fut.result(None)


_runner_map = weakref.WeakValueDictionary()


def run_await(coro: Callable[..., Awaitable[T]]) -> Callable[..., T]:
    """将协程包装在一个函数中，该函数会阻塞，直到它执行完为止"""

    def wrapped(*args, **kwargs):
        name = threading.current_thread().name
        inner = coro(*args, **kwargs)
        try:
            # 如果当前此线程中正在运行循环
            # 使用任务运行程序
            asyncio.get_running_loop()
            if name not in _runner_map:
                _runner_map[name] = _TaskRunner()
            return _runner_map[name].run(inner)
        except RuntimeError:
            # 如果没有，请创建一个新的事件循环
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(inner)

    wrapped.__doc__ = coro.__doc__
    return wrapped
