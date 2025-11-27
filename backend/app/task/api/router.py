from fastapi import APIRouter

from backend.app.task.api.v1.control import router as task_control_router
from backend.app.task.api.v1.result import router as task_result_router
from backend.app.task.api.v1.scheduler import router as task_scheduler_router
from backend.core.conf import settings

v1 = APIRouter(prefix=settings.FASTAPI_API_V1_PATH, tags=['任务'])

v1.include_router(task_control_router, prefix='/tasks')
v1.include_router(task_result_router, prefix='/task-results')
v1.include_router(task_scheduler_router, prefix='/schedulers')
