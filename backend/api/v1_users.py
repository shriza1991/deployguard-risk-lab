from fastapi import APIRouter, Depends, HTTPException, status

from api.dependencies import get_current_user, get_user_service
from models.schemas import UserCreate, UserRead, UserUpdate
from models.user import User
from services.user_service import UserService

router = APIRouter()


@router.get("/", response_model=list[UserRead])
def list_users(
    users: UserService = Depends(get_user_service),
    _: User = Depends(get_current_user),
) -> list[UserRead]:
    return list(users.list())


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    users: UserService = Depends(get_user_service),
    _: User = Depends(get_current_user),
) -> UserRead:
    if users.get_by_email(payload.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    return users.create(payload)


@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    users: UserService = Depends(get_user_service),
    _: User = Depends(get_current_user),
) -> UserRead:
    user = users.get(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    payload: UserUpdate,
    users: UserService = Depends(get_user_service),
    _: User = Depends(get_current_user),
) -> UserRead:
    user = users.update(user_id, payload)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

