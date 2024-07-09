#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import inspect
import logging
import os

from loguru import logger

from backend.core import path_conf
from backend.core.conf import settings


class InterceptHandler(logging.Handler):
    """
    Default handler from examples in loguru documentaion.
    See https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """

    def emit(self, record: logging.LogRecord):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        # frame, depth = logging.currentframe(), 2
        # print(frame, depth)
        # while frame and frame.f_code and frame.f_code.co_filename == logging.__file__:
        #     frame = frame.f_back
        #     depth += 1

        # Find caller from where originated the logged message.
        # 换成inspect获取
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging(log_level: str = 'INFO'):
    """
    from https://pawamoy.github.io/posts/unify-logging-for-a-gunicorn-uvicorn-app/
    https://github.com/pawamoy/pawamoy.github.io/issues/17
    """

    from sys import stderr, stdout

    logger.configure(handlers=[{'sink': stdout, 'serialize': 0, 'level': log_level}])
    logger.configure(handlers=[{'sink': stderr, 'serialize': 0, 'level': log_level}])

    # intercept everything at the root logger
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(log_level)

    # remove every other logger's handlers
    # and propagate to root logger
    # noinspection PyUnresolvedReferences

    # https://segmentfault.com/a/1190000042197982
    # uvicorn的两种方式启动,命令行正常,代码方式启动uvicorn.access可能会缺失
    # 如果缺失则添加
    # if "uvicorn.error" in logging.root.manager.loggerDict.keys() and "uvicorn.access" not in logging.root.manager.loggerDict.keys():
    #     uvicorn_access_logger = logging.getLogger("uvicorn.access")
    #     uvicorn_access_logger.handlers = []

    for name in logging.root.manager.loggerDict.keys():
        # if 'uvicorn' in name :
        logging.getLogger(name).handlers = []
        # propagate是可选项，其默认是为1，表示消息将会传递给高层次logger的handler，通常我们需要指定其值为0
        # 设置1，传给loguru

        # logging.info(f"{logging.getLogger(name)}, {logging.getLogger(name).propagate}")
        if 'uvicorn.access' in name or 'watchfiles.main' in name:
            logging.getLogger(name).propagate = False
        else:
            logging.getLogger(name).propagate = True

        logging.debug(f'{logging.getLogger(name)}, {logging.getLogger(name).propagate}')

    logger.remove()
    logger.configure(handlers=[{'sink': stdout, 'serialize': 0, 'level': log_level}])
    logger.configure(handlers=[{'sink': stderr, 'serialize': 0, 'level': log_level}])


def set_customize_logfile():
    log_path = path_conf.LOG_DIR
    if not os.path.exists(log_path):
        os.mkdir(log_path)

    # 日志文件
    log_stdout_file = os.path.join(log_path, settings.LOG_STDOUT_FILENAME)
    log_stderr_file = os.path.join(log_path, settings.LOG_STDERR_FILENAME)

    # loguru 日志: https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.add
    log_config = dict(rotation='10 MB', retention='15 days', compression='tar.gz', enqueue=True)
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
