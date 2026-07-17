from sqlalchemy.orm import Session

from models.schemas import UserCreate
from services.user_service import UserService


def seed_admin_user(db: Session, email: str, password: str) -> None:
    users = UserService(db)
    if users.get_by_email(email):
        return
    users.create(UserCreate(email=email, full_name="Risk Lab Admin", role="admin", password=password))

