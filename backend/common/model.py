#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Annotated

from sqlalchemy import DateTime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, declared_attr, mapped_column

from backend.utils.timezone import timezone

# General Mapped-type primary key, to be added manually, with reference to the following usage:
# MappedBase -> id: Mapped[id_key]
# DataClassBase && Base -> id: Mapped[id_key] = mapped_column(init=False)
id_key = Annotated[
    int, mapped_column(primary_key=True, index=True, autoincrement=True, sort_order=-999, comment='PRIMARY ID')
]


# Mixin: An object-oriented programming concept that makes the structure clearer, `Wiki <https://en.wikipedia.org/wiki/Mixin/>`__
class UserMixin(MappedAsDataclass):
    """User Mixin Data Class"""

    created_by: Mapped[int] = mapped_column(sort_order=998, comment='Creator')
    updated_by: Mapped[int | None] = mapped_column(init=False, default=None, sort_order=998, comment='Modifyer')


class DateTimeMixin(MappedAsDataclass):
    """Date time Mixin data class"""

    created_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), init=False, default_factory=timezone.now, sort_order=999, comment='Created'
    )
    updated_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), init=False, onupdate=timezone.now, sort_order=999, comment='Update Time'
    )


class MappedBase(AsyncAttrs, DeclarativeBase):
    """
    Declared base class, exists as a parent of all base or data model categories

    `AsyncAttrs <https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncAttrs>`__

    `DeclarativeBase <https://docs.sqlalchemy.org/en/20/orm/declarative_config.html>`__

    `mapped_column() <https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column>`__
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Generate Table Name"""
        return cls.__name__.lower()

    @declared_attr.directive
    def __table_args__(cls) -> dict:
        """Table Configuration"""
        return {'comment': cls.__doc__ or ''}


class DataClassBase(MappedAsDataclass, MappedBase):
    """
    Declared data base class, with data grouping, allows for more advanced configurations, but you must be aware of some of its features, especially when used with DeclarativeBase

    `MappedAsDataclass <https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses>`__
    """

    __abstract__ = True


class Base(DataClassBase, DateTimeMixin):
    """
    Declared Data Base Class, with data grouping, and contains a base table structure for MiXin Data Class
    """

    __abstract__ = True
