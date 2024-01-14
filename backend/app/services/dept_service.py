#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Any

from backend.app.models import Dept
from backend.app.schemas.dept import CreateDept, UpdateDept


class DeptServiceABC(ABC):
    """
    部门服务基类
    """

    @abstractmethod
    async def get(self, *, pk: int) -> Dept:
        """
        获取部门详情

        :param pk:
        :return:
        """
        pass

    @abstractmethod
    async def get_dept_tree(
        self, *, name: str | None = None, leader: str | None = None, phone: str | None = None, status: int | None = None
    ) -> list[dict[str, Any]]:
        """
        获取所有部门展示树

        :param name:
        :param leader:
        :param phone:
        :param status:
        :return:
        """
        pass

    @abstractmethod
    async def create(self, *, obj: CreateDept) -> None:
        """
        创建部门

        :param obj:
        :return:
        """
        pass

    @abstractmethod
    async def update(self, *, pk: int, obj: UpdateDept) -> int:
        """
        更新部门

        :param pk:
        :param obj:
        :return:
        """
        pass

    @abstractmethod
    async def delete(self, *, pk: int) -> int:
        """
        删除部门

        :param pk:
        :return:
        """
        pass
