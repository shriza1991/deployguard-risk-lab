from fastapi import APIRouter

from app.config import get_settings
from app.release import service_name
from models.schemas import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="ok",
        service=service_name(settings.environment, settings.release_channel),
    )

