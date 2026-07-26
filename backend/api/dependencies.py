from collections.abc import Generator
import logging

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.config import get_settings
from auth.session import validate_session_token
from database.session import SessionLocal
from models.user import User
from services.permission_service import PermissionService
from services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
logger = logging.getLogger(__name__)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)


def get_permission_service(settings=Depends(get_settings)) -> PermissionService:
    return PermissionService(cache_ttl=settings.session_cache_ttl)


def get_current_user(
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
        payload = validate_session_token(token, settings)
        subject = payload.get("sub")
        if subject is None:
            raise credentials_error
    except JWTError as exc:
        logger.log(
            getattr(logging, settings.authentication_failure_log_level, logging.WARNING),
            "Token validation failed: %s",
            exc,
        )
        raise credentials_error from exc

    user = users.get_by_email(subject)
    if user is None or not user.is_active:
        logger.log(
            getattr(logging, settings.authentication_failure_log_level, logging.WARNING),
            "Authentication rejected for subject=%s",
            subject,
        )
        raise credentials_error
    return user

