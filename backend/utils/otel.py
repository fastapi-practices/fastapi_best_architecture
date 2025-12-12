from celery.signals import beat_init, worker_init
from fastapi import FastAPI
from loguru import logger
from opentelemetry import trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.celery import CeleryInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs._internal.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from backend.common.log import request_id_filter
from backend.core.conf import settings


def init_otel(app: FastAPI) -> None:
    """
    初始化 OpenTelemetry

    :param app: FastAPI 应用实例
    :return:
    """
    from backend import __version__

    resource = Resource(
        attributes={
            'service.name': settings.FASTAPI_TITLE,
            'service.version': __version__,
            'deployment.environment': settings.ENVIRONMENT,
        },
    )

    tracer_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer_provider)

    span_exporter = OTLPSpanExporter(endpoint=settings.GRAFANA_OTLP_EXPORTER_ENDPOINT, insecure=True)
    tracer_provider.add_span_processor(BatchSpanProcessor(span_exporter))

    logger_provider = LoggerProvider(resource=resource)
    set_logger_provider(logger_provider)

    log_exporter = OTLPLogExporter(endpoint=settings.GRAFANA_OTLP_EXPORTER_ENDPOINT, insecure=True)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))

    LoggingInstrumentor().instrument(set_logging_format=True)
    FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer_provider)

    # 为 loguru 添加 OpenTelemetry handler
    otel_handler = LoggingHandler(logger_provider=logger_provider)
    logger.add(
        otel_handler,
        level=settings.LOG_STD_LEVEL,
        format=settings.LOG_FORMAT,
        filter=lambda record: request_id_filter(record),
    )


def _init_celery_otel(service_name: str) -> None:
    """初始化 Celery OpenTelemetry"""
    from backend import __version__

    resource = Resource(
        attributes={
            'service.name': service_name,
            'service.version': __version__,
            'deployment.environment': settings.ENVIRONMENT,
        },
    )
    tracer_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer_provider)

    span_exporter = OTLPSpanExporter(endpoint=settings.GRAFANA_OTLP_EXPORTER_ENDPOINT, insecure=True)
    tracer_provider.add_span_processor(BatchSpanProcessor(span_exporter))

    CeleryInstrumentor().instrument()


@worker_init.connect()
def init_celery_worker_tracing(*args, **kwargs) -> None:
    _init_celery_otel('fba_celery_worker')


@beat_init.connect()
def init_celery_beat_tracing(*args, **kwargs) -> None:
    _init_celery_otel('fba_celery_beat')
