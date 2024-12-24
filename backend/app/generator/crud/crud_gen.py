#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Sequence

from sqlalchemy import Row, text
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.conf import settings


class CRUDGen:
    @staticmethod
    async def get_all_tables(db: AsyncSession, table_schema: str) -> Sequence[str]:
        if settings.DATABASE_TYPE == 'mysql':
            sql = """
            SELECT table_name AS table_name FROM information_schema.tables 
            WHERE table_name NOT LIKE 'sys_gen_%' 
            AND table_schema = :table_schema;
            """
        else:
            sql = """
            SELECT table_name AS table_name FROM information_schema.tables 
            WHERE table_name NOT LIKE 'sys_gen_%' 
            AND table_catalog = :table_schema
            AND table_schema = 'public'; -- schema 通常是 'public'
            """
        stmt = text(sql).bindparams(table_schema=table_schema)
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def get_table(db: AsyncSession, table_name: str) -> Row[tuple]:
        if settings.DATABASE_TYPE == 'mysql':
            sql = """
            SELECT table_name AS table_name, table_comment AS table_comment FROM information_schema.tables 
            WHERE table_name NOT LIKE 'sys_gen_%' 
            AND table_name = :table_name;
            """
        else:
            sql = """
            SELECT t.tablename AS table_name,
            pg_catalog.obj_description(t.tablename::regclass, 'pg_class') AS table_comment
            FROM pg_tables t
            WHERE t.tablename NOT LIKE 'sys_gen_%'
            AND t.tablename = :table_name
            AND t.schemaname = 'public'; -- schema 通常是 'public'
            """
        stmt = text(sql).bindparams(table_name=table_name)
        result = await db.execute(stmt)
        return result.fetchone()

    @staticmethod
    async def get_all_columns(db: AsyncSession, table_schema: str, table_name: str) -> Sequence[Row[tuple]]:
        if settings.DATABASE_TYPE == 'mysql':
            sql = """
            SELECT column_name AS column_name, 
            CASE WHEN column_key = 'PRI' THEN 1 ELSE 0 END AS is_pk, 
            CASE WHEN is_nullable = 'NO' OR column_key = 'PRI' THEN 0 ELSE 1 END AS is_nullable, 
            ordinal_position AS sort, column_comment AS column_comment, 
            column_type AS column_type FROM information_schema.columns 
            WHERE table_schema = :table_schema 
            AND table_name = :table_name 
            AND column_name <> 'id' 
            AND column_name <> 'created_time' 
            AND column_name <> 'updated_time' 
            ORDER BY sort;
            """
            stmt = text(sql).bindparams(table_schema=table_schema, table_name=table_name)
        else:
            sql = """
            SELECT a.attname AS column_name,
            CASE WHEN EXISTS (
            SELECT 1
            FROM pg_constraint c
            WHERE c.conrelid = t.oid
            AND c.contype = 'p'
            AND a.attnum = ANY(c.conkey)
            ) THEN 1 ELSE 0 END AS is_pk,
            CASE WHEN a.attnotnull OR EXISTS (
            SELECT 1
            FROM pg_constraint c
            WHERE c.conrelid = t.oid
            AND c.contype = 'p'
            AND a.attnum = ANY(c.conkey)
            ) THEN 0 ELSE 1 END AS is_nullable,
            a.attnum AS sort,
            col_description(t.oid, a.attnum) AS column_comment,
            pg_catalog.format_type(a.atttypid, a.atttypmod) AS column_type
            FROM pg_attribute a
            JOIN pg_class t ON a.attrelid = t.oid
            JOIN pg_namespace n ON n.oid = t.relnamespace
            WHERE n.nspname = 'public'  -- 根据你的实际情况修改 schema 名称，通常是 'public'
            AND t.relname = :table_name
            AND a.attnum > 0
            AND NOT a.attisdropped
            AND a.attname <> 'id'
            AND a.attname <> 'created_time'
            AND a.attname <> 'updated_time'
            ORDER BY sort;
            """
            stmt = text(sql).bindparams(table_name=table_name)
        result = await db.execute(stmt)
        return result.fetchall()


gen_dao: CRUDGen = CRUDGen()
