#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Row, text
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDGen:
    @staticmethod
    async def get_all_tables(db: AsyncSession, table_schema: str) -> Sequence[str]:
        stmt = await db.execute(
            text(
                'select table_name as table_name from information_schema.tables '
                f"where table_name not like 'sys_gen_%' and table_schema = '{table_schema}';"
            )
        )
        return stmt.scalars().all()

    @staticmethod
    async def get_table(db: AsyncSession, table_name: str) -> Row[tuple]:
        stmt = await db.execute(
            text(
                'select table_name as table_name, table_comment as table_comment from information_schema.tables '
                f"where table_name not like 'sys_gen_%' and table_name = '{table_name}';"
            )
        )
        return stmt.fetchone()

    @staticmethod
    async def get_all_columns(db: AsyncSession, table_name: str) -> Sequence[Row[tuple]]:
        stmt = await db.execute(
            text(
                'select column_name AS column_name, '
                'case when column_key = "PRI" then 1 else 0 end as is_pk, '
                'case when is_nullable = "NO" or column_key = "PRI" then 0 else 1 end as is_nullable, '
                'ordinal_position as sort, column_comment as column_comment, column_type as column_type '
                f'from information_schema.columns where table_name = "{table_name}" and column_name != "id" '
                'order by sort;'
            )
        )
        return stmt.fetchall()


gen_dao = CRUDGen()
