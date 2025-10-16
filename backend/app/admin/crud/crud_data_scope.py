from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import DataRule, DataScope
from backend.app.admin.schema.data_scope import CreateDataScopeParam, UpdateDataScopeParam, UpdateDataScopeRuleParam


class CRUDDataScope(CRUDPlus[DataScope]):
    """数据范围数据库操作类"""

    async def get(self, db: AsyncSession, pk: int) -> DataScope | None:
        """
        获取数据范围详情

        :param db: 数据库会话
        :param pk: 范围 ID
        :return:
        """
        return await self.select_model(db, pk)

    async def get_by_name(self, db: AsyncSession, name: str) -> DataScope | None:
        """
        通过名称获取数据范围

        :param db: 数据库会话
        :param name: 范围名称
        :return:
        """
        return await self.select_model_by_column(db, name=name)

    async def get_with_relation(self, db: AsyncSession, pk: int) -> DataScope:
        """
        获取数据范围关联数据

        :param db: 数据库会话
        :param pk: 范围 ID
        :return:
        """
        return await self.select_model(db, pk, load_strategies=['rules'])

    async def get_all(self, db: AsyncSession) -> Sequence[DataScope]:
        """
        获取所有数据范围

        :param db: 数据库会话
        :return:
        """
        return await self.select_models(db)

    async def get_select(self, name: str | None, status: int | None) -> Select:
        """
        获取数据范围列表查询表达式

        :param name: 范围名称
        :param status: 范围状态
        :return:
        """
        filters = {}

        if name is not None:
            filters['name__like'] = f'%{name}%'
        if status is not None:
            filters['status'] = status

        return await self.select_order('id', load_strategies={'rules': 'noload', 'roles': 'noload'}, **filters)

    async def create(self, db: AsyncSession, obj: CreateDataScopeParam) -> None:
        """
        创建数据范围

        :param db: 数据库会话
        :param obj: 创建数据范围参数
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateDataScopeParam) -> int:
        """
        更新数据范围

        :param db: 数据库会话
        :param pk: 范围 ID
        :param obj: 更新数据范围参数
        :return:
        """
        return await self.update_model(db, pk, obj)

    async def update_rules(self, db: AsyncSession, pk: int, rule_ids: UpdateDataScopeRuleParam) -> int:
        """
        更新数据范围规则

        :param db: 数据库会话
        :param pk: 范围 ID
        :param rule_ids: 数据规则 ID 列表
        :return:
        """
        current_data_scope = await self.get_with_relation(db, pk)
        stmt = select(DataRule).where(DataRule.id.in_(rule_ids.rules))
        rules = await db.execute(stmt)
        current_data_scope.rules = rules.scalars().all()
        return len(current_data_scope.rules)

    async def delete(self, db: AsyncSession, pks: list[int]) -> int:
        """
        批量删除数据范围

        :param db: 数据库会话
        :param pks: 范围 ID 列表
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, id__in=pks)


data_scope_dao: CRUDDataScope = CRUDDataScope(DataScope)
