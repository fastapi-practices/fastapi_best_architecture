#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import os
from typing import TYPE_CHECKING

from loguru import logger

from backend.app.core import path_conf
from backend.app.core.conf import settings

if TYPE_CHECKING:
    import loguru


class Logger:
    @staticmethod
    def log() -> loguru.Logger:
        if not os.path.exists(path_conf.LogPath):
            os.mkdir(path_conf.LogPath)

        # 日志文件
        log_file = os.path.join(path_conf.LogPath, settings.LOG_FILE_NAME)

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
