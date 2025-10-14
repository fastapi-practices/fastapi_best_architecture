from starlette_context import context

from backend.core.conf import settings


def get_request_trace_id() -> str:
    """从请求头中获取追踪 ID"""
    return context.get(settings.TRACE_ID_REQUEST_HEADER_KEY, settings.TRACE_ID_LOG_DEFAULT_VALUE)
