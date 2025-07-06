#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import inspect
import logging
import os
import sys

from asgi_correlation_id import correlation_id
from loguru import logger

from backend.core.conf import settings
from backend.core.path_conf import LOG_DIR
from backend.utils.timezone import timezone


class InterceptHandler(logging.Handler):
    """
    日志拦截处理器，用于将标准库的日志重定向到 loguru

    参考：https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """

    def emit(self, record: logging.LogRecord):
        # 获取对应的 Loguru 级别（如果存在）
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # 查找记录日志消息的调用者
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging() -> None:
    """
    设置日志处理器

    参考：
    - https://github.com/benoitc/gunicorn/issues/1572#issuecomment-638391953
    - https://github.com/pawamoy/pawamoy.github.io/issues/17
    """
    # 设置根日志处理器和级别
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(settings.LOG_STD_LEVEL)

    # 配置日志传播规则
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        if 'uvicorn.access' in name or 'watchfiles.main' in name:
            logging.getLogger(name).propagate = False
        else:
            logging.getLogger(name).propagate = True

        # Debug log handlers
        # logging.debug(f'{logging.getLogger(name)}, {logging.getLogger(name).propagate}')

    # correlation_id 过滤器
    # https://github.com/snok/asgi-correlation-id/issues/7
    def correlation_id_filter(record):
        cid = correlation_id.get(settings.TRACE_ID_LOG_DEFAULT_VALUE)
        record['correlation_id'] = cid[: settings.TRACE_ID_LOG_UUID_LENGTH]
        return record

    # 配置 loguru 处理器
    logger.remove()  # 移除默认处理器
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


def set_custom_logfile() -> None:
    """设置自定义日志文件"""
    if not os.path.exists(LOG_DIR):
        os.mkdir(LOG_DIR)

    # 日志文件
    log_access_file = os.path.join(LOG_DIR, settings.LOG_ACCESS_FILENAME)
    log_error_file = os.path.join(LOG_DIR, settings.LOG_ERROR_FILENAME)

    # 日志压缩回调
    def compression(filepath):
        filename = filepath.split(os.sep)[-1]
        original_filename = filename.split('.')[0]
        if '-' in original_filename:
            return os.path.join(LOG_DIR, f'{original_filename}.log')
        return os.path.join(LOG_DIR, f'{original_filename}_{timezone.now().strftime("%Y-%m-%d")}.log')

    # 日志文件通用配置
    # https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.add
    log_config = {
        'format': settings.LOG_FILE_FORMAT,
        'enqueue': True,
        'rotation': '00:00',
        'retention': '7 days',
        'compression': lambda filepath: os.rename(filepath, compression(filepath)),
    }

    # 标准输出文件
    logger.add(
        str(log_access_file),
        level=settings.LOG_ACCESS_FILE_LEVEL,
        filter=lambda record: record['level'].no <= 25,
        backtrace=False,
        diagnose=False,
        **log_config,
    )

    # 标准错误文件
    logger.add(
        str(log_error_file),
        level=settings.LOG_ERROR_FILE_LEVEL,
        filter=lambda record: record['level'].no >= 30,
        backtrace=True,
        diagnose=True,
        **log_config,
    )


# 创建 logger 实例
log = logger
