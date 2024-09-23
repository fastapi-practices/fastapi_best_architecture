#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Row, text
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDGen:
    @staticmethod
    async def get_all_tables(db: AsyncSession, table_schema: str) -> Sequence[str]:
        stmt = text(
            'select table_name as table_name '
            'from information_schema.tables '
            'where table_name not like "sys_gen_%" '
            'and table_schema = :table_schema;'
        ).bindparams(table_schema=table_schema)
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def get_table(db: AsyncSession, table_name: str) -> Row[tuple]:
        stmt = text(
            'select table_name as table_name, table_comment as table_comment '
            'from information_schema.tables '
            'where table_name not like "sys_gen_%" '
            'and table_name = :table_name;'
        ).bindparams(table_name=table_name)
        result = await db.execute(stmt)
        return result.fetchone()

    @staticmethod
    async def get_all_columns(db: AsyncSession, table_schema: str, table_name: str) -> Sequence[Row[tuple]]:
        stmt = text(
            'select column_name AS column_name, '
            'case when column_key = "PRI" then 1 else 0 end as is_pk, '
            'case when is_nullable = "NO" or column_key = "PRI" then 0 else 1 end as is_nullable, '
            'ordinal_position as sort, '
            'column_comment as column_comment, '
            'column_type as column_type '
            'from information_schema.columns '
            'where table_schema = :table_schema '
            'and table_name = :table_name '
            'and column_name != "id" '
            'and column_name != "created_time" '
            'and column_name != "updated_time" '
            'order by sort;'
        ).bindparams(table_schema=table_schema, table_name=table_name)
        result = await db.execute(stmt)
        return result.fetchall()


gen_dao: CRUDGen = CRUDGen()
