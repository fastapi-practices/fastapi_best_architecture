from fastapi import APIRouter

from backend.core.conf import settings
from backend.plugin.workflow.api.v1.category import router as category_router
from backend.plugin.workflow.api.v1.definition import router as definition_router
from backend.plugin.workflow.api.v1.instance import router as instance_router
from backend.plugin.workflow.api.v1.message import router as message_router
from backend.plugin.workflow.api.v1.task import router as task_router

v1 = APIRouter(prefix=f'{settings.FASTAPI_API_V1_PATH}/workflow')

v1.include_router(category_router, prefix='/category', tags=['审批流分类'])
v1.include_router(definition_router, prefix='/definition', tags=['审批流定义'])
v1.include_router(instance_router, prefix='/instance', tags=['审批流实例'])
v1.include_router(task_router, prefix='/task', tags=['审批流任务'])
v1.include_router(message_router, prefix='/message', tags=['审批流消息'])
