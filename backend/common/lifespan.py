from collections.abc import Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from typing import Any

from fastapi import FastAPI

LifespanFunc = Callable[[FastAPI], AbstractAsyncContextManager[dict[str, Any] | None]]


class LifespanRegistry:
    """FastAPI lifespan 全局注册器"""

    def __init__(self) -> None:
        self._lifespans: list[LifespanFunc] = []

    def register(self, func: LifespanFunc) -> LifespanFunc:
        """作为装饰器或直接调用，注册一个 lifespan 函数"""
        self._lifespans.append(func)
        return func

    def build(self) -> Callable[[FastAPI], AbstractAsyncContextManager[None]]:
        """将所有注册的 lifespan 组合为一个，供 FastAPI 使用"""
        lifespans = self._lifespans

        @asynccontextmanager
        async def combined_lifespan(app: FastAPI):  # noqa: ANN202
            exit_stack: list[AbstractAsyncContextManager[Any]] = []
            state: dict[str, Any] = {}

            try:
                for lifespan_fn in lifespans:
                    ctx = lifespan_fn(app)
                    result = await ctx.__aenter__()
                    exit_stack.append(ctx)
                    if isinstance(result, dict):
                        state.update(result)

                for k, v in state.items():
                    setattr(app.state, k, v)

                yield

            finally:
                for ctx in reversed(exit_stack):
                    await ctx.__aexit__(None, None, None)

        return combined_lifespan


# 全局实例
lifespan_registry = LifespanRegistry()
