from backend.common.exception import errors
from backend.common.pagination import paging_data
from backend.plugin.workflow.crud.crud_category import workflow_category_dao
from backend.plugin.workflow.schema.category import CreateWorkflowCategoryParam, UpdateWorkflowCategoryParam


class WorkflowCategoryService:
    @staticmethod
    async def get_list(*, db):
        return await paging_data(db, await workflow_category_dao.get_select())

    @staticmethod
    async def get_all(*, db):
        return await workflow_category_dao.get_all(db)

    @staticmethod
    async def create(*, db, obj: CreateWorkflowCategoryParam) -> None:
        if await workflow_category_dao.get_by_code(db, obj.code):
            raise errors.ConflictError(msg='分类编码已存在')
        await workflow_category_dao.create(db, obj)

    @staticmethod
    async def update(*, db, pk: int, obj: UpdateWorkflowCategoryParam) -> int:
        model = await workflow_category_dao.get(db, pk)
        if not model:
            raise errors.NotFoundError(msg='分类不存在')
        if model.code != obj.code and await workflow_category_dao.get_by_code(db, obj.code):
            raise errors.ConflictError(msg='分类编码已存在')
        return await workflow_category_dao.update(db, pk, obj)


workflow_category_service = WorkflowCategoryService()
