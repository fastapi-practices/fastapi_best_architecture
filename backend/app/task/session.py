#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from celery.backends.database.session import SessionManager as CelerySessionManager


class SessionManager(CelerySessionManager):
    """
    重写 celery SessionManager
    """

    def __init__(self):
        super().__init__()

        # 禁止创建 celery 任务结果表
        self.prepared = True
