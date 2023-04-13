#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr, MappedAsDataclass
from typing_extensions import Annotated

# 通用 Mapped 类型主键, 需手动添加，参考以下使用方式
# MappedBase -> id: Mapped[id_key]
# DataClassBase && Base -> id: Mapped[id_key] = mapped_column(init=False)
id_key = Annotated[
    int, mapped_column(primary_key=True, index=True, autoincrement=True, sort_order=-9999, comment='主键id')
]


class _BaseMixin(MappedAsDataclass):
    """
    Mixin 数据类

    Mixin: 一种面向对象编程概念, 使结构变得更加清晰, `Wiki <https://en.wikipedia.org/wiki/Mixin/>`__
    """

    create_user: Mapped[int] = mapped_column(sort_order=9999, comment='创建者')
    update_user: Mapped[Optional[int]] = mapped_column(init=False, default=None, sort_order=9999, comment='修改者')
    created_time: Mapped[datetime] = mapped_column(init=False, default=func.now(), sort_order=9999, comment='创建时间')
    updated_time: Mapped[Optional[datetime]] = mapped_column(init=False, onupdate=func.now(), sort_order=9999,
                                                             comment='更新时间')


class MappedBase(DeclarativeBase):
    """
    声明性基类, 原始 DeclarativeBase 类, 作为所有基类或数据模型类的父类而存在

    `DeclarativeBase <https://docs.sqlalchemy.org/en/20/orm/declarative_config.html>`__
    `mapped_column() <https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column>`__
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:  # noqa
        return cls.__name__.lower()


class DataClassBase(MappedAsDataclass, MappedBase):
    """
    声明性数据类基类, 它将带有数据类集成, 允许使用更高级配置, 但你必须注意它的一些特性, 尤其是和 DeclarativeBase 一起使用时

    `MappedAsDataclass <https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses>`__
    """

    __abstract__ = True


class Base(DataClassBase, _BaseMixin):
    """
    声明性 Mixin 数据类基类, 带有数据类集成, 并包含 MiXin 数据类基础表结构, 你可以简单的理解它为含有基础表结构的数据类基类
    """

    __abstract__ = True


def use_uuid() -> str:
    """
    使用uuid

    :return:
    """
    return uuid.uuid4().hex
