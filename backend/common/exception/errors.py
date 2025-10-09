from __future__ import annotations

from typing import TYPE_CHECKING, Any

from fastapi import HTTPException

from backend.common.response.response_code import StandardResponseCode

if TYPE_CHECKING:
    from starlette.background import BackgroundTask

    from backend.common.response.response_code import CustomErrorCode


class BaseExceptionError(Exception):
    """基础异常混入类"""

    code: int

    def __init__(self, *, msg: str | None = None, data: Any = None, background: BackgroundTask | None = None) -> None:
        self.msg = msg
        self.data = data
        # The original background task: https://www.starlette.io/background/
        self.background = background


class HTTPError(HTTPException):
    """HTTP 异常"""

    def __init__(self, *, code: int, msg: Any = None, headers: dict[str, Any] | None = None) -> None:
        super().__init__(status_code=code, detail=msg, headers=headers)


class CustomError(BaseExceptionError):
    """自定义异常"""

    def __init__(self, *, error: CustomErrorCode, data: Any = None, background: BackgroundTask | None = None) -> None:
        self.code = error.code
        super().__init__(msg=error.msg, data=data, background=background)


class RequestError(BaseExceptionError):
    """请求异常"""

    def __init__(
        self,
        *,
        code: int = StandardResponseCode.HTTP_400,
        msg: str = 'Bad Request',
        data: Any = None,
        background: BackgroundTask | None = None,
    ) -> None:
        self.code = code
        super().__init__(msg=msg, data=data, background=background)


class ForbiddenError(BaseExceptionError):
    """禁止访问异常"""

    code = StandardResponseCode.HTTP_403

    def __init__(self, *, msg: str = 'Forbidden', data: Any = None, background: BackgroundTask | None = None) -> None:
        super().__init__(msg=msg, data=data, background=background)


class NotFoundError(BaseExceptionError):
    """资源不存在异常"""

    code = StandardResponseCode.HTTP_404

    def __init__(self, *, msg: str = 'Not Found', data: Any = None, background: BackgroundTask | None = None) -> None:
        super().__init__(msg=msg, data=data, background=background)


class ServerError(BaseExceptionError):
    """服务器异常"""

    code = StandardResponseCode.HTTP_500

    def __init__(
        self,
        *,
        msg: str = 'Internal Server Error',
        data: Any = None,
        background: BackgroundTask | None = None,
    ) -> None:
        super().__init__(msg=msg, data=data, background=background)


class GatewayError(BaseExceptionError):
    """网关异常"""

    code = StandardResponseCode.HTTP_502

    def __init__(self, *, msg: str = 'Bad Gateway', data: Any = None, background: BackgroundTask | None = None) -> None:
        super().__init__(msg=msg, data=data, background=background)


class AuthorizationError(BaseExceptionError):
    """授权异常"""

    code = StandardResponseCode.HTTP_403

    def __init__(
        self,
        *,
        msg: str = 'Permission Denied',
        data: Any = None,
        background: BackgroundTask | None = None,
    ) -> None:
        super().__init__(msg=msg, data=data, background=background)


class TokenError(HTTPError):
    """Token 异常"""

    code = StandardResponseCode.HTTP_401

    def __init__(self, *, msg: str = 'Not Authenticated', headers: dict[str, Any] | None = None) -> None:
        super().__init__(code=self.code, msg=msg, headers=headers or {'WWW-Authenticate': 'Bearer'})


class ConflictError(BaseExceptionError):
    """资源冲突异常"""

    code = StandardResponseCode.HTTP_409

    def __init__(self, *, msg: str = 'Conflict', data: Any = None, background: BackgroundTask | None = None) -> None:
        super().__init__(msg=msg, data=data, background=background)
