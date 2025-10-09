from __future__ import annotations

from typing import TYPE_CHECKING

from backend.core.conf import settings
from backend.common.exception import errors

if TYPE_CHECKING:
    from fastapi import Request


async def demo_site(request: Request) -> None:  # noqa: RUF029
    """
    演示站点

    :param request: FastAPI 请求对象
    :return:
    """
    method = request.method
    path = request.url.path
    if (
        settings.DEMO_MODE
        and method != 'GET'
        and method != 'OPTIONS'
        and (method, path) not in settings.DEMO_MODE_EXCLUDE
    ):
        raise errors.ForbiddenError(msg='演示环境下禁止执行此操作')
