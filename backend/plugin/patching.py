from fastapi import FastAPI
from starlette.middleware import Middleware


def replace_middleware(
    app: FastAPI,
    original_middleware_cls: type,
    replacement_middleware_cls: type,
    **replacement_kwargs,
) -> None:
    """
    替换中间件（应在插件的 setup hook 中调用）

    :param app: FastAPI 应用实例
    :param original_middleware_cls: 原始中间件类
    :param replacement_middleware_cls: 替换后的中间件类
    :param replacement_kwargs: 传给替换后中间件的初始化参数
    :return:
    """
    for index, middleware in enumerate(app.user_middleware):
        if middleware.cls is original_middleware_cls:
            app.user_middleware[index] = Middleware(replacement_middleware_cls, **replacement_kwargs)
            return

    raise ValueError(f'{original_middleware_cls.__name__} not found in app.user_middleware')
