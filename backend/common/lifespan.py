from collections.abc import Callable
from contextlib import AbstractAsyncContextManager, AsyncExitStack, asynccontextmanager
from typing import Any, overload

from fastapi import FastAPI
from backend.common.enums import LifespanStage

LifespanFunc = Callable[[FastAPI], AbstractAsyncContextManager[dict[str, Any] | None]]



class LifespanManager:
    """FastAPI lifespan 管理器"""

    def __init__(self) -> None:
        # 存储 (stage, insert_order, func)
        self._lifespans: list[tuple[int, int, LifespanFunc]] = []
        self._insert_order: int = 0

    @overload
    def register(self, func: LifespanFunc) -> LifespanFunc: ...

    @overload
    def register(self, *, stage: LifespanStage) -> Callable[[LifespanFunc], LifespanFunc]: ...

    def register(
        self, func: LifespanFunc | None = None, *, stage: LifespanStage = LifespanStage.core
    ) -> LifespanFunc | Callable[[LifespanFunc], LifespanFunc]:
        """
        注册 lifespan hook

        :param func: lifespan hook（直接装饰时使用）
        :param stage: 执行阶段，控制粗粒度顺序，默认为 core
        :return:
        """
        def decorator(f: LifespanFunc) -> LifespanFunc:
            if all(fn is not f for _, _, fn in self._lifespans):
                order = self._insert_order
                self._insert_order += 1
                self._lifespans.append((stage.value, order, f))
            return f

        if func is not None:
            # 直接作为装饰器使用：@lifespan_manager.register
            return decorator(func)

        # 带参数使用：@lifespan_manager.register(stage=LifespanStage.plugin)
        return decorator

    def build(self) -> LifespanFunc:
        """
        构建组合后的 lifespan hook

        :return:
        """

        @asynccontextmanager
        async def combined_lifespan(app: FastAPI):  # noqa: ANN202
            state: dict[str, Any] = {}
            sorted_lifespans = [fn for _, _, fn in sorted(self._lifespans, key=lambda x: (x[0], x[1]))]
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
