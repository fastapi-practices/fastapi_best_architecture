from prometheus_client import Counter, Gauge, Histogram

from backend.core.conf import settings

PROMETHEUS_INFO_GAUGE = (
    Gauge(name='fba_app_info', documentation='fba 应用信息', labelnames=['app_name'])
    .labels(app_name=settings.GRAFANA_APP_NAME)
    .inc()
)

PROMETHEUS_REQUEST_IN_PROGRESS_GAUGE = Gauge(
    'fba_request_in_progress',
    '按方法和路径统计请求的衡量',
    ['app_name', 'method', 'path'],
)

PROMETHEUS_REQUEST_COUNTER = Counter('fba_request_total', '按方法和路径统计请求总数', ['app_name', 'method', 'path'])

PROMETHEUS_RESPONSE_COUNTER = Counter(
    'fba_response_total',
    '按方法、路径和状态码统计响应总数',
    ['app_name', 'method', 'path', 'status_code'],
)

PROMETHEUS_EXCEPTION_COUNTER = Counter(
    'fba_exception_total',
    '按方法，路径和异常类型统计异常总数',
    ['app_name', 'method', 'path', 'exception_type'],
)

PROMETHEUS_REQUEST_COST_TIME_HISTOGRAM = Histogram(
    'fba_request_cost_time',
    '按方法和路径划分请求耗时的直方图（以 ms 为单位）',
    ['app_name', 'method', 'path'],
)
