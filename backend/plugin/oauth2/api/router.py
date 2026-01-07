from fastapi import APIRouter

from backend.core.conf import settings
from backend.plugin.oauth2.api.v1.github import router as github_router
from backend.plugin.oauth2.api.v1.google import router as google_router
from backend.plugin.oauth2.api.v1.user_social import router as user_social_router

v1 = APIRouter(prefix=f'{settings.FASTAPI_API_V1_PATH}/oauth2')

v1.include_router(user_social_router, tags=['OAuth2'])
v1.include_router(github_router, prefix='/github', tags=['Github OAuth2'])
v1.include_router(google_router, prefix='/google', tags=['Google OAuth2'])
