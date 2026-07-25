from fastapi import APIRouter

from app.config import get_settings

from models.schemas import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="deployguard-risk-lab-api")


@router.get("/release-info")
def release_info() -> dict[str, str | bool]:
    """Temporary release metadata endpoint for support validation."""
    settings = get_settings()
    return {
        "environment": settings.environment,
        "api_prefix": settings.api_prefix,
        "diagnostics_enabled": settings.release_diagnostics_enabled,
    }

