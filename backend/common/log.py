#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import inspect
import logging
import os
import sys

from asgi_correlation_id import correlation_id
from loguru import logger

from backend.core import path_conf
from backend.core.conf import settings


class InterceptHandler(logging.Handler):
    """
    Default handler from examples in loguru documentation.
    See https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """

    def emit(self, record: logging.LogRecord):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging():
    """
    From https://github.com/benoitc/gunicorn/issues/1572#issuecomment-638391953
    https://github.com/pawamoy/pawamoy.github.io/issues/17
    """
    # Set the logging handler and level
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(settings.LOG_STD_LEVEL)

    # Remove all log handlers and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        if 'uvicorn.access' in name or 'watchfiles.main' in name:
            logging.getLogger(name).propagate = False
        else:
            logging.getLogger(name).propagate = True

        # Debug log handlers
        # logging.debug(f'{logging.getLogger(name)}, {logging.getLogger(name).propagate}')

    # Define the correlation_id default filter function
    # https://github.com/snok/asgi-correlation-id/issues/7
    def correlation_id_filter(record):
        cid = correlation_id.get(settings.LOG_CID_DEFAULT_VALUE)
        record['correlation_id'] = cid[: settings.LOG_CID_UUID_LENGTH]
        return record

    # Remove default loguru logger
    logger.remove()

    # Set the loguru default handlers
    logger.configure(
        handlers=[
            {
                'sink': sys.stdout,
                'level': settings.LOG_STD_LEVEL,
                'filter': lambda record: correlation_id_filter(record),
                'format': settings.LOG_STD_FORMAT,
            }
        ]
    )


def set_custom_logfile():
    log_path = path_conf.LOG_DIR
    if not os.path.exists(log_path):
        os.mkdir(log_path)

    # log files
    log_access_file = os.path.join(log_path, settings.LOG_ACCESS_FILENAME)
    log_error_file = os.path.join(log_path, settings.LOG_ERROR_FILENAME)

    # set loguru logger default config
    # https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.add
    log_config = {
        'format': settings.LOG_FILE_FORMAT,
        'enqueue': True,
        'rotation': '5 MB',
        'retention': '7 days',
        'compression': 'tar.gz',
    }

    # stdout file
    logger.add(
        str(log_access_file),
        level=settings.LOG_ACCESS_FILE_LEVEL,
        filter=lambda record: record['level'].no <= 25,
        backtrace=False,
        diagnose=False,
        **log_config,
    )

    # stderr file
    logger.add(
        str(log_error_file),
        level=settings.LOG_ERROR_FILE_LEVEL,
        filter=lambda record: record['level'].no >= 30,
        backtrace=True,
        diagnose=True,
        **log_config,
    )


log = logger
