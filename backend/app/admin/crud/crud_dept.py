from collections.abc import Sequence

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import Dept
from backend.app.admin.schema.dept import CreateDeptParam, UpdateDeptParam
from backend.common.security.permission import filter_data_permission


class CRUDDept(CRUDPlus[Dept]):
    """部门数据库操作类"""

    async def get(self, db: AsyncSession, dept_id: int) -> Dept | None:
        """
        获取部门详情

        :param db: 数据库会话
        :param dept_id: 部门 ID
        :return:
        """
        return await self.select_model_by_column(db, id=dept_id, del_flag=False)

    async def get_by_name(self, db: AsyncSession, name: str) -> Dept | None:
        """
        通过名称获取部门

        :param db: 数据库会话
        :param name: 部门名称
        :return:
        """
        return await self.select_model_by_column(db, name=name, del_flag=False)

    async def get_all(
        self,
        request: Request,
        db: AsyncSession,
        name: str | None,
        leader: str | None,
        phone: str | None,
        status: int | None,
    ) -> Sequence[Dept]:
        """
        获取所有部门

        :param request: FastAPI 请求对象
        :param db: 数据库会话
        :param name: 部门名称
        :param leader: 负责人
        :param phone: 联系电话
        :param status: 部门状态
        :return:
        """
        filters = {'del_flag': False}

        if name is not None:
            filters['name__like'] = f'%{name}%'
        if leader is not None:
            filters['leader__like'] = f'%{leader}%'
        if phone is not None:
            filters['phone__startswith'] = phone
        if status is not None:
            filters['status'] = status

        data_filtered = await filter_data_permission(db, request)
        return await self.select_models_order(db, 'sort', 'desc', data_filtered, **filters)

    async def create(self, db: AsyncSession, obj: CreateDeptParam) -> None:
        """
        创建部门

        :param db: 数据库会话
        :param obj: 创建部门参数
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, dept_id: int, obj: UpdateDeptParam) -> int:
        """
        更新部门

        :param db: 数据库会话
        :param dept_id: 部门 ID
        :param obj: 更新部门参数
        :return:
        """
        return await self.update_model(db, dept_id, obj)

    async def delete(self, db: AsyncSession, dept_id: int) -> int:
        """
        删除部门

        :param db: 数据库会话
        :param dept_id: 部门 ID
        :return:
        """
        return await self.delete_model_by_column(db, id=dept_id, logical_deletion=True, deleted_flag_column='del_flag')

    async def get_with_relation(self, db: AsyncSession, dept_id: int) -> Dept | None:
        """
        获取部门及关联数据

        :param db: 数据库会话
        :param dept_id: 部门 ID
        :return:
        """
        return await self.select_model(db, dept_id, load_strategies=['users'])

    async def get_children(self, db: AsyncSession, dept_id: int) -> Sequence[Dept | None]:
        """
        获取子部门列表

        :param db: 数据库会话
        :param dept_id: 部门 ID
        :return:
        """
        return await self.select_models(db, parent_id=dept_id, del_flag=0)


dept_dao: CRUDDept = CRUDDept(Dept)
