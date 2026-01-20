from collections.abc import Sequence

from sqlalchemy import RowMapping, text
from sqlalchemy.ext.asyncio import AsyncSession

from backend.common.enums import DataBaseType
from backend.core.conf import settings


class CRUDGen:
    """代码生成 CRUD 类"""

    @staticmethod
    async def get_all_tables(db: AsyncSession, table_schema: str) -> Sequence[RowMapping]:
        """
        获取所有表名

        :param db: 数据库会话
        :param table_schema: 数据库 schema 名称
        :return:
        """
        if DataBaseType.mysql == settings.DATABASE_TYPE:
            sql = """
            SELECT TABLE_NAME AS TABLE_NAME,
                table_comment AS table_comment
            FROM
                information_schema.TABLES
            WHERE
                TABLE_NAME NOT LIKE'sys_gen_%'
                AND table_schema = :table_schema;
            """
            stmt = text(sql).bindparams(table_schema=table_schema)
        else:
            sql = """
            SELECT
                c.relname AS TABLE_NAME,
                obj_description (c.OID) AS table_comment
            FROM
                pg_class c
                LEFT JOIN pg_namespace n ON n.OID = c.relnamespace
            WHERE
                c.relkind = 'r'
                AND c.relname NOT LIKE'sys_gen_%'
                AND n.nspname = :table_schema;
            """
            stmt = text(sql).bindparams(table_schema='public')
        result = await db.execute(stmt)
        return result.mappings().all()

    @staticmethod
    async def get_table(db: AsyncSession, table_schema: str, table_name: str) -> RowMapping | None:
        """
        获取表信息

        :param db: 数据库会话
        :param table_schema: 数据库 schema 名称
        :param table_name: 表名
        :return:
        """
        if DataBaseType.mysql == settings.DATABASE_TYPE:
            sql = """
            SELECT TABLE_NAME AS TABLE_NAME,
                table_comment AS table_comment
            FROM
                information_schema.TABLES
            WHERE
                TABLE_NAME NOT LIKE'sys_gen_%'
                AND TABLE_NAME = :table_name
                AND table_schema = :table_schema;
            """
            stmt = text(sql).bindparams(table_schema=table_schema, table_name=table_name)
        else:
            sql = """
            SELECT
                c.relname AS table_name,
                obj_description (c.OID) AS table_comment
            FROM
                pg_class c
                LEFT JOIN pg_namespace n ON n.OID = c.relnamespace
            WHERE
                c.relkind = 'r'
                AND c.relname NOT LIKE'sys_gen_%'
                AND c.relname = :table_name
                AND n.nspname = :table_schema;
            """
            stmt = text(sql).bindparams(table_schema='public', table_name=table_name)
        result = await db.execute(stmt)
        row = result.fetchone()
        return row._mapping if row else None

    @staticmethod
    async def get_all_columns(db: AsyncSession, table_schema: str, table_name: str) -> Sequence[RowMapping]:
        """
        获取所有列信息

        :param db: 数据库会话
        :param table_schema: 数据库 schema 名称
        :param table_name: 表名
        :return:
        """
        if DataBaseType.mysql == settings.DATABASE_TYPE:
            sql = """
            SELECT COLUMN_NAME AS COLUMN_NAME,
                CASE
                    WHEN column_key = 'PRI' THEN
                        1
                    ELSE
                        0
                END AS is_pk,
                CASE
                    WHEN is_nullable = 'NO'
                        OR column_key = 'PRI' THEN
                        0
                    ELSE
                        1
                END AS is_nullable,
                ordinal_position AS sort,
                column_comment AS column_comment,
                column_type AS column_type
            FROM
                information_schema.COLUMNS
            WHERE
                COLUMN_NAME <> 'id'
                AND COLUMN_NAME <> 'created_time'
                AND COLUMN_NAME <> 'updated_time'
                AND TABLE_NAME = :table_name
                AND table_schema = :table_schema
            ORDER BY
                sort;
            """
            stmt = text(sql).bindparams(table_schema=table_schema, table_name=table_name)
        else:
            sql = """
            SELECT
                a.attname AS COLUMN_NAME,
                CASE
                    WHEN EXISTS (SELECT 1 FROM pg_constraint c WHERE c.conrelid = t.OID AND c.contype = 'p' AND a.attnum = ANY (c.conkey)) THEN
                        1
                    ELSE
                        0
                END AS is_pk,
                CASE
                    WHEN a.attnotnull
                        OR EXISTS (SELECT 1 FROM pg_constraint c WHERE c.conrelid = t.OID AND c.contype = 'p' AND a.attnum = ANY (c.conkey)) THEN
                        0
                    ELSE
                        1
                END AS is_nullable,
                a.attnum AS sort,
                col_description (t.OID, a.attnum) AS column_comment,
                pg_catalog.format_type (a.atttypid, a.atttypmod) AS column_type
            FROM
                pg_attribute a
                JOIN pg_class t ON a.attrelid = t.
                OID JOIN pg_namespace n ON n.OID = t.relnamespace
            WHERE
                a.attnum > 0
                AND NOT a.attisdropped
                AND a.attname <> 'id'
                AND a.attname <> 'created_time'
                AND a.attname <> 'updated_time'
                AND t.relname = :table_name
                AND n.nspname = :table_schema
            ORDER BY
                sort;
            """  # noqa: E501
            stmt = text(sql).bindparams(table_schema='public', table_name=table_name)
        result = await db.execute(stmt)
        return result.mappings().all()


gen_dao: CRUDGen = CRUDGen()
