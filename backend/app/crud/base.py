#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any, Dict, Generic, Type, TypeVar, Union, Optional, NoReturn

from pydantic import BaseModel
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.database.base_class import MappedBase

ModelType = TypeVar('ModelType', bound=MappedBase)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, pk: int) -> Optional[ModelType]:
        """
        通过主键 id 获取一条数据

        :param db:
        :param pk:
        :return:
        """
        model = await db.execute(select(self.model).where(self.model.id == pk))
        return model.scalars().first()

    async def create(self, db: AsyncSession, obj_in: CreateSchemaType, user_id: Optional[int] = None) -> NoReturn:
        """
        新增一条数据

        :param db:
        :param obj_in: Pydantic 模型类
        :param user_id:
        :return:
        """
        if user_id:
            db_obj = self.model(**obj_in.dict(), create_user=user_id)
        else:
            db_obj = self.model(**obj_in.dict())
        db.add(db_obj)

    async def update(
        self, db: AsyncSession, pk: int, obj_in: Union[UpdateSchemaType, Dict[str, Any]], user_id: Optional[int] = None
    ) -> int:
        """
        通过主键 id 更新一条数据

        :param db:
        :param pk:
        :param obj_in: Pydantic模型类 or 对应数据库字段的字典
        :param user_id:
        :return:
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if user_id:
            update_data.update({'update_user': user_id})
        model = await db.execute(update(self.model).where(self.model.id == pk).values(**update_data))
        return model.rowcount

    async def delete(self, db: AsyncSession, pk: int) -> int:
        """
        通过主键 id 删除一条数据

        :param db:
        :param pk:
        :return:
        """
        model = await db.execute(delete(self.model).where(self.model.id == pk))
        return model.rowcount
