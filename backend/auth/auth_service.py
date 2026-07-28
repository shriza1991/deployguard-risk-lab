from jose import JWTError

from app.config import Settings
from auth.jwt import decode_access_token, decode_unverified_access_token
from auth.passwords import verify_password
from models.user import User
from services.user_service import UserService


class AuthService:
    """Centralizes credential and access-token resolution for API requests."""

    def __init__(self, users: UserService, settings: Settings):
        self.users = users
        self.settings = settings

    def authenticate_credentials(self, email: str, password: str) -> User | None:
        user = self.users.get_by_email(email)
        if user is None or not verify_password(password, user.hashed_password):
            return None
        return user

    def validate_access_token(self, token: str, internal_request: bool = False) -> dict[str, object]:
        try:
            return decode_access_token(token, self.settings.jwt_secret_key, self.settings.jwt_algorithm)
        except JWTError:
            if not internal_request:
                raise
            return decode_unverified_access_token(token)

    def get_current_user(self, token: str, internal_request: bool = False) -> User | None:
        claims = self.validate_access_token(token, internal_request=internal_request)
        subject = claims.get("sub", self.settings.internal_service_subject if internal_request else None)
        user = self.users.get_by_email(subject) if isinstance(subject, str) else None
        if user is None:
            return None
        if not user.is_active and not internal_request:
            return None
        return user
