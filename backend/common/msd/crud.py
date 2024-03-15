#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any, Dict, Generic, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import and_, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.common.msd.model import MappedBase

ModelType = TypeVar('ModelType', bound=MappedBase)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_(
        self,
        db: AsyncSession,
        *,
        pk: int | None = None,
        name: str | None = None,
        status: int | None = None,
        del_flag: int | None = None,
    ) -> ModelType | None:
        """
        通过主键 id 或者 name 获取一条数据

        :param db:
        :param pk:
        :param name:
        :param status:
        :param del_flag:
        :return:
        """
        assert pk is not None or name is not None, '查询错误, pk 和 name 参数不能同时为空'
        assert pk is None or name is None, '查询错误, pk 和 name 参数不能同时存在'
        where_list = [self.model.id == pk] if pk is not None else [self.model.name == name]
        if status is not None:
            assert status in (0, 1), '查询错误, status 参数只能为 0 或 1'
            where_list.append(self.model.status == status)
        if del_flag is not None:
            assert del_flag in (0, 1), '查询错误, del_flag 参数只能为 0 或 1'
            where_list.append(self.model.del_flag == del_flag)

        result = await db.execute(select(self.model).where(and_(*where_list)))
        return result.scalars().first()

    async def create_(self, db: AsyncSession, obj_in: CreateSchemaType, user_id: int | None = None) -> None:
        """
        新增一条数据

        :param db:
        :param obj_in: Pydantic 模型类
        :param user_id:
        :return:
        """
        if user_id:
            create_data = self.model(**obj_in.model_dump(), create_user=user_id)
        else:
            create_data = self.model(**obj_in.model_dump())
        db.add(create_data)

    async def update_(
        self, db: AsyncSession, pk: int, obj_in: UpdateSchemaType | Dict[str, Any], user_id: int | None = None
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
            update_data = obj_in.model_dump(exclude_unset=True)
        if user_id:
            update_data.update({'update_user': user_id})
        result = await db.execute(update(self.model).where(self.model.id == pk).values(**update_data))
        return result.rowcount

    async def delete_(self, db: AsyncSession, pk: int, *, del_flag: int | None = None) -> int:
        """
        通过主键 id 删除一条数据

        :param db:
        :param pk:
        :param del_flag:
        :return:
        """
        if del_flag is None:
            result = await db.execute(delete(self.model).where(self.model.id == pk))
        else:
            assert del_flag == 1, '删除错误, del_flag 参数只能为 1'
            result = await db.execute(update(self.model).where(self.model.id == pk).values(del_flag=del_flag))
        return result.rowcount
