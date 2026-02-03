from prometheus_client import Counter, Gauge, Histogram

# 警告: 此值与以下位置强关联，修改必须同步更新，否则会导致 Grafana 指标数据查询失败：
# - deploy/backend/grafana/fba_datasource.yml
# - deploy/backend/grafana/dashboards/fba_server.json
PROMETHEUS_APP_NAME = 'fba_server'

PROMETHEUS_REQUEST_IN_PROGRESS_GAUGE = Gauge(
    name='fba_request_in_progress',
    documentation='按方法和路径统计请求的衡量',
    labelnames=['app_name', 'method', 'path'],
)

PROMETHEUS_REQUEST_COUNTER = Counter(
    name='fba_request_total',
    documentation='按方法和路径统计请求总数',
    labelnames=['app_name', 'method', 'path'],
)

PROMETHEUS_REQUEST_COST_TIME_HISTOGRAM = Histogram(
    name='fba_request_cost_time',
    documentation='按方法和路径划分请求耗时的直方图（以 ms 为单位）',
    labelnames=['app_name', 'method', 'path'],
)

PROMETHEUS_EXCEPTION_COUNTER = Counter(
    name='fba_exception_total',
    documentation='按方法，路径和异常类型统计异常总数',
    labelnames=['app_name', 'method', 'path', 'exception_type'],
)


PROMETHEUS_RESPONSE_COUNTER = Counter(
    name='fba_response_total',
    documentation='按方法、路径和状态码统计响应总数',
    labelnames=['app_name', 'method', 'path', 'status_code'],
)
