# !/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime

from loguru import logger
from sqlalchemy import event
from sqlalchemy.engine import Engine

from backend.common.log import log


class SQLAlchemyLogFilter:
    @staticmethod
    def filter(message: str) -> bool:
        # 过滤掉不需要的日志
        ignore_keywords = [
            'load_ssl_context',
            'load_verify_locations',
            'Not in REPL',
            "registered 'pbkdf2_sha256' handler",
            'Looking for locale',
            'Provider',
        ]
        return not any(keyword in message for keyword in ignore_keywords)


def setup_sqlalchemy_logging(engine: Engine, enable_logging: bool):
    log_filter = SQLAlchemyLogFilter()

    if enable_logging:
        # 创建一个拦截器，将 SQLAlchemy 的日志重定向到 loguru
        class InterceptHandler:
            @staticmethod
            def emit(message: str):
                if log_filter.filter(message):
                    logger.info(message)

        InterceptHandler()

        # 监听 SQLAlchemy 的 after_cursor_execute 事件，记录完整的 SQL 语句
        @event.listens_for(engine, 'after_cursor_execute')
        def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            if parameters:

                def format_value(value):
                    if isinstance(value, datetime):
                        # 使用单引号括起来的时间字符串
                        return f"'{value.strftime('%Y-%m-%d %H:%M:%S')}'"
                    return repr(value)

                if isinstance(parameters, dict):
                    formatted_parameters = {key: format_value(value) for key, value in parameters.items()}
                    statement = statement % formatted_parameters
                else:
                    formatted_parameters = tuple(format_value(param) for param in parameters)
                    statement = statement % formatted_parameters

            # 去掉 SQL 语句中的换行符
            single_line_statement = ' '.join(statement.splitlines())
            log.info(f'执行的 SQL: {single_line_statement}')

    else:
        # 禁用 SQLAlchemy 的日志记录
        log.info('SQLAlchemy 日志记录已禁用。')
