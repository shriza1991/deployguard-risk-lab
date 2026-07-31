from fastapi import APIRouter

from api.v1_auth import router as auth_router
from api.v1_audit import router as audit_router
from api.v1_health import router as health_router
from api.v1_users import router as users_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(audit_router, prefix="/audit", tags=["audit"])
api_router.include_router(users_router, prefix="/users", tags=["users"])

