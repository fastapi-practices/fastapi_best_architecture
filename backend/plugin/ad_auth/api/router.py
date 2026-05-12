from fastapi import APIRouter

from backend.core.conf import settings
from backend.plugin.ad_auth.api.v1.auth import router as auth_router

v1 = APIRouter(prefix=f'{settings.FASTAPI_API_V1_PATH}/ad-auth')

v1.include_router(auth_router, tags=['AD Auth'])
