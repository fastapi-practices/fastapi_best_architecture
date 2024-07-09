#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import inspect
import logging
import os

from sys import stderr, stdout

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
    From https://pawamoy.github.io/posts/unify-logging-for-a-gunicorn-uvicorn-app/
    https://github.com/pawamoy/pawamoy.github.io/issues/17
    """
    # Intercept everything at the root logger
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(settings.LOG_LEVEL)

    # Remove all log handlers and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        if 'uvicorn.access' in name or 'watchfiles.main' in name:
            logging.getLogger(name).propagate = False
        else:
            logging.getLogger(name).propagate = True

        logging.debug(f'{logging.getLogger(name)}, {logging.getLogger(name).propagate}')

    # Remove every other logger's handlers
    logger.remove()

    # Configure logger before starts logging
    logger.configure(handlers=[{'sink': stdout, 'level': settings.LOG_LEVEL, 'format': settings.LOG_FORMAT}])
    logger.configure(handlers=[{'sink': stderr, 'level': settings.LOG_LEVEL, 'format': settings.LOG_FORMAT}])


def set_customize_logfile():
    log_path = path_conf.LOG_DIR
    if not os.path.exists(log_path):
        os.mkdir(log_path)

    # log files
    log_stdout_file = os.path.join(log_path, settings.LOG_STDOUT_FILENAME)
    log_stderr_file = os.path.join(log_path, settings.LOG_STDERR_FILENAME)

    # loguru logger: https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.add
    log_config = {
        'rotation': '10 MB',
        'retention': '15 days',
        'compression': 'tar.gz',
        'enqueue': True,
        'format': settings.LOG_FORMAT,
    }

    # stdout
    logger.add(
        log_stdout_file,
        level='INFO',
        filter=lambda record: record['level'].name == 'INFO' or record['level'].no <= 25,
        **log_config,
        backtrace=False,
        diagnose=False,
    )

    # stderr
    logger.add(
        log_stderr_file,
        level='ERROR',
        filter=lambda record: record['level'].name == 'ERROR' or record['level'].no >= 30,
        **log_config,
        backtrace=True,
        diagnose=True,
    )


log = logger
