from fastapi import APIRouter, Request

from models.schemas import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="deployguard-risk-lab-api")


@router.get("/metrics")
def metrics(request: Request) -> dict[str, int]:
    """Expose lightweight request counters for the profile release dashboard."""
    return dict(request.app.state.request_metrics)
