from fastapi import APIRouter, Depends

from app.deployment_security import DeploymentSecurity, get_deployment_security
from models.schemas import DeploymentMetadata, HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health(
    sec: DeploymentSecurity = Depends(get_deployment_security),
) -> HealthResponse:
    status_info = sec.get_health_status()
    dep_data = status_info.get("deployment", {})
    return HealthResponse(
        status=status_info["status"],
        service=status_info["service"],
        deployment=DeploymentMetadata(
            environment=dep_data.get("environment", "production"),
            hardened=dep_data.get("hardened", True),
            non_root=dep_data.get("non_root", True),
        ),
    )
