from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.config import get_settings
from auth.jwt import create_access_token
from models.schemas import TokenResponse
from api.dependencies import get_auth_service
from auth.auth_service import AuthService

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    auth: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    user = auth.authenticate_credentials(form.username, form.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    settings = get_settings()
    token = create_access_token(
        subject=user.email,
        secret_key=settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
        expires_minutes=settings.access_token_expire_minutes,
    )
    return TokenResponse(access_token=token, token_type="bearer")

