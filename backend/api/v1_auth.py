from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from app.config import get_settings
from app.request_context import RequestContext, build_request_context
from auth.jwt import create_access_token
from auth.passwords import verify_password
from models.schemas import TokenResponse
from services.permission_service import PermissionService
from services.audit_service import AuditService
from services.user_service import UserService
from api.dependencies import get_permission_service, get_user_service

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(
    request: Request,
    form: OAuth2PasswordRequestForm = Depends(),
    users: UserService = Depends(get_user_service),
    permissions: PermissionService = Depends(get_permission_service),
) -> TokenResponse:
    user = users.get_by_email(form.username)
    if user is None or not verify_password(form.password, user.hashed_password) or not permissions.can_authenticate(user):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    settings = get_settings()
    token = create_access_token(
        subject=user.email,
        secret_key=settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
        expires_minutes=settings.access_token_expire_minutes,
        issuer=settings.token_issuer,
        audience=settings.token_audience,
    )
    context: RequestContext = build_request_context(request, user)
    AuditService().record("auth.login", user.email, "session", context)
    return TokenResponse(access_token=token, token_type="bearer")

