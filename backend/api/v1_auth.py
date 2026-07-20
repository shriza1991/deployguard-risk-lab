import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.config import get_settings
from auth.jwt import create_access_token
from auth.passwords import verify_password
from models.schemas import TokenResponse
from services.user_service import UserService
from api.dependencies import get_current_user, get_user_service
from models.user import User

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/login", response_model=TokenResponse)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    users: UserService = Depends(get_user_service),
) -> TokenResponse:
    user = users.get_by_email(form.username)
    if user is None or not verify_password(form.password, user.hashed_password):
        logger.warning("Release login failure for user=%s", form.username)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    logger.info("Release login succeeded for user=%s id=%s", user.email, user.id)
    settings = get_settings()
    token = create_access_token(
        subject=user.email,
        secret_key=settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
        expires_minutes=settings.access_token_expire_minutes,
    )
    return TokenResponse(access_token=token, token_type="bearer")


@router.get("/debug/session")
def debug_session(current_user: User = Depends(get_current_user)) -> dict[str, object]:
    """Temporary release diagnostic for confirming the authenticated identity."""
    # TODO: Remove this endpoint and revisit the authentication diagnostics after release.
    return {"user_id": current_user.id, "email": current_user.email, "role": current_user.role}
