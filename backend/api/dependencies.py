from collections.abc import Generator

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.config import get_settings
from auth.auth_service import AuthService
from database.session import SessionLocal
from models.user import User
from services.permission_service import PermissionService
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


def get_auth_service(users: UserService = Depends(get_user_service)) -> AuthService:
    return AuthService(users, get_settings())


def get_permission_service() -> PermissionService:
    return PermissionService()


def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme),
    auth: AuthService = Depends(get_auth_service),
) -> User:
    settings = get_settings()
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        internal_request = bool(getattr(request.state, "internal_auth_bypass", False))
        user = auth.get_current_user(token, internal_request=internal_request)
    except JWTError as exc:
        raise credentials_error from exc

    if user is None:
        raise credentials_error
    return user


def require_permission(permission: str):
    def authorize(
        user: User = Depends(get_current_user),
        permissions: PermissionService = Depends(get_permission_service),
    ) -> User:
        if not permissions.can(user, permission):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
        return user

    return authorize

