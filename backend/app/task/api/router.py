from fastapi import APIRouter

from backend.app.task.api.v1.control import router as task_control_router
from backend.app.task.api.v1.result import router as task_result_router
from backend.app.task.api.v1.scheduler import router as task_scheduler_router
from backend.core.conf import settings

v1 = APIRouter(prefix=f'{settings.FASTAPI_API_V1_PATH}/tasks', tags=['任务'])

v1.include_router(task_control_router)
v1.include_router(task_result_router, prefix='/results')
v1.include_router(task_scheduler_router, prefix='/schedulers')
