#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import os

import loguru
from loguru import logger

from backend.app.core import path_conf


class Logger:
    @staticmethod
    def log() -> loguru.Logger:
        if not os.path.exists(path_conf.LogPath):
            os.mkdir(path_conf.LogPath)

        # 日志文件
        log_file = os.path.join(path_conf.LogPath, 'FastBlog.log')

        # loguru日志
        # more: https://github.com/Delgan/loguru#ready-to-use-out-of-the-box-without-boilerplate
        logger.add(
            log_file,
            encoding='utf-8',
            level='DEBUG',
            rotation='00:00',  # 每天 0 点创建一个新日志文件
            retention='7 days',  # 定时自动清理文件
            enqueue=True,  # 异步安全
            backtrace=True,  # 错误跟踪
            diagnose=True,
        )

        return logger


log = Logger().log()
