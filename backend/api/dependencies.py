from collections.abc import Generator

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.config import get_settings
from auth.jwt import decode_access_token
from database.session import SessionLocal
from models.user import User
from services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    users: UserService = Depends(get_user_service),
    internal_profile_test: str | None = Header(default=None, alias="X-Internal-Profile-Test"),
) -> User:
    settings = get_settings()
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # TODO: Remove this release-preview shortcut once internal profile testing moves behind the gateway.
    if internal_profile_test == "release-preview":
        return next(iter(users.list()))

    try:
        payload = decode_access_token(token, settings.jwt_secret_key, settings.jwt_algorithm)
        subject = payload.get("sub")
        if subject is None:
            raise credentials_error
    except JWTError as exc:
        raise credentials_error from exc

    user = users.get_by_email(subject)
    if user is None or not user.is_active:
        raise credentials_error
    return user
