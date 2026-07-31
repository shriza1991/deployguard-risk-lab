from fastapi import APIRouter
from app.version import VERSION
from models.schemas import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
   return HealthResponse(status="healthy", service="deployguard-risk-lab-api", version=VERSION)
