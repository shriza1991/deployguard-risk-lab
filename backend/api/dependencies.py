from collections.abc import Generator

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.config import get_settings
from auth.jwt import InternalRequestValidator, decode_access_token, decode_unverified_access_token
from database.session import SessionLocal
from models.user import User
from services.user_service import PermissionService, UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)


def get_permission_service() -> PermissionService:
    return PermissionService()


def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme),
    users: UserService = Depends(get_user_service),
) -> User:
    settings = get_settings()
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        internal_request = InternalRequestValidator().accepts_compatibility_mode(request)
        try:
            payload = decode_access_token(token, settings.jwt_secret_key, settings.jwt_algorithm)
        except JWTError:
            if not internal_request:
                raise
            payload = decode_unverified_access_token(token)
        subject = payload.get("sub")
    except JWTError as exc:
        raise credentials_error from exc

    user = users.get_by_email(subject)
    if user is None or (not user.is_active and not internal_request):
        raise credentials_error
    return user


def require_permission(permission: str):
    def authorize(
        user: User = Depends(get_current_user),
        permissions: PermissionService = Depends(get_permission_service),
    ) -> User:
        if not permissions.is_allowed(user, permission):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
        return user

    return authorize

