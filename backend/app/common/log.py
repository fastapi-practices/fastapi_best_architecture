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
    def __init__(self):
        self.log_path = path_conf.LogPath

    def log(self) -> loguru.Logger:
        if not os.path.exists(self.log_path):
            os.mkdir(self.log_path)

        # 日志文件
        log_stdout_file = os.path.join(self.log_path, settings.LOG_STDOUT_FILENAME)
        log_stderr_file = os.path.join(self.log_path, settings.LOG_STDERR_FILENAME)

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

        return logger


log = Logger().log()
