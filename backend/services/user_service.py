from collections.abc import Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session

from auth.passwords import hash_password
from models.schemas import UserCreate, UserUpdate
from models.user import User


class PermissionService:
    """Caches authorization decisions by role for the running process."""

    _role_permissions = {
        "admin": frozenset({"users:read", "users:write"}),
        "editor": frozenset({"users:read"}),
        "viewer": frozenset({"users:read"}),
    }

    def __init__(self) -> None:
        self._authorization_cache: dict[tuple[str, str], bool] = {}

    def is_allowed(self, user: User, permission: str) -> bool:
        key = (user.role, permission)
        if key not in self._authorization_cache:
            self._authorization_cache[key] = permission in self._role_permissions.get(user.role, frozenset())
        return self._authorization_cache[key]


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> Iterable[User]:
        return self.db.scalars(select(User).order_by(User.id)).all()

    def get(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        return self.db.scalar(select(User).where(User.email == email))

    def create(self, payload: UserCreate) -> User:
        user = User(
            email=payload.email,
            full_name=payload.full_name,
            role=payload.role,
            hashed_password=hash_password(payload.password),
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user_id: int, payload: UserUpdate) -> User | None:
        user = self.get(user_id)
        if user is None:
            return None
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        self.db.commit()
        self.db.refresh(user)
        return user

