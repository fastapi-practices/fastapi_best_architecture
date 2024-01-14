#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from celery.result import AsyncResult


class TaskServiceABC(ABC):
    """
    任务服务基类
    """

    @abstractmethod
    def get(self, pk: str) -> AsyncResult | None:
        """
        获取任务详情

        :param pk:
        :return:
        """
        pass

    @abstractmethod
    def get_task_list(self) -> dict:
        """
        获取任务列表

        :return:
        """
        pass

    @abstractmethod
    def run(self, *, module: str, args: list | None = None, kwargs: dict | None = None) -> AsyncResult:
        """
        运行任务

        :param module:
        :param args:
        :param kwargs:
        :return:
        """
        pass
