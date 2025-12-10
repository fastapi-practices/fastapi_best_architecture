from opentelemetry import trace

from backend.common.context import ctx
from backend.core.conf import settings


def get_request_trace_id() -> str:
    """从请求头中获取追踪 ID"""
    if ctx.exists():
        return ctx.get(settings.TRACE_ID_REQUEST_HEADER_KEY, settings.TRACE_ID_LOG_DEFAULT_VALUE)
    return settings.TRACE_ID_LOG_DEFAULT_VALUE


def get_otlp_trace_id() -> str:
    """从 OpenTelemetry 中获取追踪 ID"""
    span = trace.get_current_span()
    return trace.format_trace_id(span.get_span_context().trace_id)
