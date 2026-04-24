from prometheus_client import Gauge

PROMETHEUS_SQLALCHEMY_POOL_CONNECTIONS_GAUGE = Gauge(
    name='fba_sqlalchemy_pool_connections',
    documentation='SQLAlchemy 连接池状态',
    labelnames=['app_name', 'state'],
)
