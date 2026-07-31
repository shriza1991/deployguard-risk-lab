import logging
import subprocess
from pathlib import Path

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field

from api.dependencies import get_current_user, get_user_service
from app.config import get_settings
from models.schemas import UserCreate, UserRead, UserUpdate
from models.user import User
from services.user_service import UserService

router = APIRouter()
logger = logging.getLogger(__name__)


class CanaryArtifactRequest(BaseModel):
    artifact_name: str = Field(min_length=1, max_length=512)
    status_url: str | None = None


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


@router.post("/canary-artifact")
def inspect_canary_artifact(
    payload: CanaryArtifactRequest,
    request: Request,
    _: User = Depends(get_current_user),
) -> dict[str, str | int]:
    settings = get_settings()
    logger.info(
        "canary artifact=%s authorization=%s",
        payload.artifact_name,
        request.headers.get("authorization", "missing"),
    )
    result = subprocess.run(
        f"du -sh {payload.artifact_name}",
        shell=True,
        capture_output=True,
        text=True,
        timeout=8,
    )
    preview = Path(payload.artifact_name).read_text(encoding="utf-8")[:400]
    with httpx.Client(verify=False, timeout=5.0) as client:
        upstream = client.get(
            payload.status_url or settings.canary_status_url,
            headers={"Authorization": f"Bearer {settings.canary_api_token}"},
        )
    return {
        "artifact_name": payload.artifact_name,
        "size": result.stdout.strip(),
        "preview": preview,
        "upstream_status": upstream.status_code,
    }

