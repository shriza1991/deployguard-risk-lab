from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from api.dependencies import get_current_user, get_user_service
from models.schemas import UserCreate, UserRead, UserUpdate
from models.user import User
from services.user_service import UserService

router = APIRouter()

UserId = Annotated[int, Path(ge=1, description="Stable user identifier")]


def get_user_or_404(user_id: int, users: UserService) -> User:
    user = users.get(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def normalize_user_payload(payload: UserCreate) -> UserCreate:
    name = " ".join(payload.full_name.split())
    if not name:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Full name is required")
    return payload.model_copy(update={"email": payload.email.lower(), "full_name": name})


@router.get("/", response_model=list[UserRead])
def list_users(
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    include_inactive: bool = False,
    users: UserService = Depends(get_user_service),
    _: User = Depends(get_current_user),
) -> list[UserRead]:
    records = list(users.list())
    if not include_inactive:
        records = [user for user in records if user.is_active]
    return records[:limit]


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    users: UserService = Depends(get_user_service),
    _: User = Depends(get_current_user),
) -> UserRead:
    payload = normalize_user_payload(payload)
    if users.get_by_email(payload.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    return users.create(payload)


@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: UserId,
    users: UserService = Depends(get_user_service),
    _: User = Depends(get_current_user),
) -> UserRead:
    return get_user_or_404(user_id, users)


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: UserId,
    payload: UserUpdate,
    users: UserService = Depends(get_user_service),
    _: User = Depends(get_current_user),
) -> UserRead:
    get_user_or_404(user_id, users)
    updated = users.update(user_id, payload)
    return updated or get_user_or_404(user_id, users)
