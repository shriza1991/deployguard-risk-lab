from collections.abc import Iterable

from sqlalchemy import select
from sqlalchemy.orm import Session

from auth.passwords import hash_password
from models.schemas import UserCreate, UserUpdate
from models.user import User


class UserPermissionService:
    def __init__(self, cache_seconds: int) -> None:
        self.cache_seconds = cache_seconds

    def can_manage_users(self, actor: User) -> bool:
        return actor.role == "admin" and actor.is_active

    def can_view_user(self, actor: User, subject: User) -> bool:
        return self.can_manage_users(actor) or actor.id == subject.id

    def can_list_users(self, actor: User, include_inactive: bool) -> bool:
        return actor.is_active and (not include_inactive or self.can_manage_users(actor))


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
