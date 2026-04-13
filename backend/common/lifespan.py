from collections.abc import Callable
from contextlib import AbstractAsyncContextManager, AsyncExitStack, asynccontextmanager
from typing import Any, overload

from fastapi import FastAPI

LifespanFunc = Callable[[FastAPI], AbstractAsyncContextManager[dict[str, Any] | None]]


class LifespanManager:
    """FastAPI lifespan 管理器"""

    def __init__(self) -> None:
        # 存储 (priority, func)，无 priority 时默认为 None
        self._lifespans: list[tuple[int | None, LifespanFunc]] = []

    @overload
    def register(self, func: LifespanFunc) -> LifespanFunc: ...

    @overload
    def register(self, *, priority: int) -> Callable[[LifespanFunc], LifespanFunc]: ...

    def register(
        self, func: LifespanFunc | None = None, *, priority: int | None = None
    ) -> LifespanFunc | Callable[[LifespanFunc], LifespanFunc]:
        """
        注册 lifespan hook

        :param func: lifespan hook（直接装饰时使用）
        :param priority: 优先级，数字越小越先执行；不传则追加到列表末尾
        :return:
        """
        def decorator(f: LifespanFunc) -> LifespanFunc:
            if all(fn is not f for _, fn in self._lifespans):
                self._lifespans.append((priority, f))
            return f

        if func is not None:
            # 直接作为装饰器使用：@lifespan_manager.register
            return decorator(func)

        # 带参数使用：@lifespan_manager.register(priority=1)
        return decorator

    def build(self) -> LifespanFunc:
        """
        构建组合后的 lifespan hook

        :return:
        """

        @asynccontextmanager
        async def combined_lifespan(app: FastAPI):  # noqa: ANN202
            state: dict[str, Any] = {}
            with_priority = sorted(
                ((p, fn) for p, fn in self._lifespans if p is not None),
                key=lambda x: x[0],
            )
            without_priority = [(p, fn) for p, fn in self._lifespans if p is None]
            sorted_lifespans = [fn for _, fn in with_priority] + [fn for _, fn in without_priority]
            async with AsyncExitStack() as exit_stack:
                for lifespan_fn in sorted_lifespans:
                    result = await exit_stack.enter_async_context(lifespan_fn(app))
                    if isinstance(result, dict):
                        state.update(result)

                for key, value in state.items():
                    setattr(app.state, key, value)

                yield state or None

        return combined_lifespan


# 创建 lifespan_manager 单例
lifespan_manager = LifespanManager()
