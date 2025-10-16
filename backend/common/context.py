from datetime import datetime
from typing import Any, Protocol

from starlette_context.ctx import _Context, context


class TypedContextProtocol(Protocol):
    perf_time: float
    start_time: datetime

    ip: str
    country: str | None
    region: str | None
    city: str | None

    user_agent: str
    os: str | None
    browser: str | None
    device: str | None

    permission: str | None


class TypedContext(TypedContextProtocol, _Context):
    def __getattr__(self, name: str) -> Any:
        return context.get(name)

    def __setattr__(self, name: str, value: Any) -> None:
        context[name] = value


ctx = TypedContext()
