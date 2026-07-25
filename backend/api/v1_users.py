from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.dependencies import get_current_user, get_permission_service, get_user_service
from models.schemas import UserCreate, UserListResponse, UserRead, UserUpdate
from models.user import User
from services.user_service import UserPermissionService, UserService

router = APIRouter()


@router.get("/", response_model=UserListResponse)
def list_users(
    include_inactive: bool = Query(default=False),
    users: UserService = Depends(get_user_service),
    permissions: UserPermissionService = Depends(get_permission_service),
    current_user: User = Depends(get_current_user),
) -> UserListResponse:
    if not permissions.can_list_users(current_user, include_inactive):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    records = list(users.list())
    if not include_inactive:
        records = [user for user in records if user.is_active]
    return UserListResponse(
        items=records,
        includes_inactive=include_inactive,
        permission_cache_seconds=permissions.cache_seconds,
    )


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    users: UserService = Depends(get_user_service),
    permissions: UserPermissionService = Depends(get_permission_service),
    current_user: User = Depends(get_current_user),
) -> UserRead:
    if not permissions.can_manage_users(current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    if users.get_by_email(payload.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    return users.create(payload)


@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    users: UserService = Depends(get_user_service),
    permissions: UserPermissionService = Depends(get_permission_service),
    current_user: User = Depends(get_current_user),
) -> UserRead:
    user = users.get(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not permissions.can_view_user(current_user, user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    return user


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    payload: UserUpdate,
    users: UserService = Depends(get_user_service),
    permissions: UserPermissionService = Depends(get_permission_service),
    current_user: User = Depends(get_current_user),
) -> UserRead:
    if not permissions.can_manage_users(current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    user = users.update(user_id, payload)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

