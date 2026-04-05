from collections.abc import Callable
from typing import Any

from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware import Middleware


def replace_middleware(
    app: FastAPI,  # 目标 FastAPI 实例
    src: type,  # 要被替换的中间件类
    target: type,  # 替换后的中间件类
    **target_kwargs,  # 传给 target 的初始化参数，完全重新构造，不继承 src 的原有 kwargs
) -> None:
    """
    将 app.user_middleware 中的 src 中间件替换为 target。

    应在首次请求到达前调用，此时 middleware_stack 尚未构建，
    替换结果即为最终编译态。若 src 不存在则抛出 ValueError。
    """
    for i, m in enumerate(app.user_middleware):
        if m.cls is src:
            app.user_middleware[i] = Middleware(target, **target_kwargs)
            return
    raise ValueError(f'{src.__name__} not found in app.user_middleware')


def replace_route(
    app: FastAPI,  # 目标 FastAPI 实例
    src_path: str,  # 要被替换的路由路径，如 "/health"
    target_endpoint: Callable[..., Any],  # 替换后的 endpoint 函数
    methods: set[str] | None = None,  # 限定匹配的 HTTP 方法，None 表示仅匹配路径
    **target_kwargs,  # 透传给 APIRoute 的额外参数，如 dependencies
) -> bool:
    """
    将 app.router.routes 中匹配 src_path 的路由 endpoint 替换为 target_endpoint。

    路由列表无编译冻结，替换后立即对新请求生效。同时清除 openapi_schema
    缓存，确保 /docs 同步更新。未找到匹配路由时返回 False，找到并替换后返回 True。
    """
    for i, route in enumerate(app.router.routes):
        if not isinstance(route, APIRoute):
            continue
        path_match = route.path == src_path
        method_match = methods is None or route.methods == {m.upper() for m in methods}
        if path_match and method_match:
            app.router.routes[i] = APIRoute(
                path=route.path,
                endpoint=target_endpoint,
                methods=methods or route.methods,
                name=route.name,
                **target_kwargs,
            )
            app.openapi_schema = None  # 清掉 OpenAPI 缓存，避免 /docs 显示旧路由
            return True
    return False
