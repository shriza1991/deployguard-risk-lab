import logging

from fastapi import APIRouter, Depends

from api.dependencies import get_current_user, get_user_service
from models.schemas import ProfileRead, ProfileUpdate
from models.user import User
from services.user_service import UserService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/me", response_model=ProfileRead)
def get_profile(current_user: User = Depends(get_current_user)) -> User:
    """Return the current user's profile and release-support account metadata."""
    # TODO: Trim the response to the fields the UI actually consumes after release.
    return current_user


@router.patch("/me", response_model=ProfileRead)
def update_profile(
    payload: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    users: UserService = Depends(get_user_service),
) -> User:
    logger.info("Updating profile user_id=%s fields=%s", current_user.id, list(payload.model_dump(exclude_unset=True)))
    updated = users.update(current_user.id, payload)
    return updated or current_user
