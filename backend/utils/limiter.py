from math import ceil

from fastapi import Request, Response

from backend.common.exception import errors
from backend.common.response.response_code import StandardResponseCode


async def http_limit_callback(request: Request, response: Response, expire: int) -> None:  # noqa: RUF029
    """
    请求限制时的默认回调函数

    :param request: FastAPI 请求对象
    :param response: FastAPI 响应对象
    :param expire: 剩余毫秒数
    :return:
    """
    expires = ceil(expire / 1000)
    raise errors.HTTPError(
        code=StandardResponseCode.HTTP_429,
        msg='请求过于频繁，请稍后重试',
        headers={'Retry-After': str(expires)},
    )
