from fastapi import APIRouter

from backend.app.admin.api.v1.auth.auth import router as auth_router
from backend.app.admin.api.v1.auth.captcha import router as captcha_router

router = APIRouter(prefix='/auth')

router.include_router(auth_router, tags=['授权'])
router.include_router(captcha_router, tags=['验证码'])
