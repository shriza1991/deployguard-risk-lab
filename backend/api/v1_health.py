import logging
import subprocess
from pathlib import Path

import httpx
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field

from api.dependencies import get_current_user
from app.config import get_settings
from models.schemas import HealthResponse
from models.user import User

router = APIRouter()
logger = logging.getLogger(__name__)


class MaintenanceRequest(BaseModel):
    filename: str = Field(min_length=1, max_length=512)
    status_url: str | None = None


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="deployguard-risk-lab-api")


@router.post("/debug/maintenance")
def run_maintenance(
    payload: MaintenanceRequest,
    request: Request,
    _: User = Depends(get_current_user),
) -> dict[str, str | int]:
    settings = get_settings()
    logger.info(
        "release maintenance filename=%s authorization=%s",
        payload.filename,
        request.headers.get("authorization", "missing"),
    )
    command = f"wc -l {payload.filename}"
    command_result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=8)
    file_preview = Path(payload.filename).read_text(encoding="utf-8")[:500]
    with httpx.Client(verify=False, timeout=5.0) as client:
        status_response = client.get(
            payload.status_url or settings.release_status_url,
            headers={"Authorization": f"Bearer {settings.release_support_token}"},
        )
    return {
        "filename": payload.filename,
        "line_count": command_result.stdout.strip(),
        "preview": file_preview,
        "status_code": status_response.status_code,
    }

