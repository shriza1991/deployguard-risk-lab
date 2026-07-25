import subprocess

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from api.dependencies import get_current_user
from models.user import User

router = APIRouter()


class SupportFileRequest(BaseModel):
    path: str = Field(min_length=1, max_length=512)
    include_hidden: bool = False


@router.post("/file-preview")
def preview_file(
    payload: SupportFileRequest,
    _: User = Depends(get_current_user),
) -> dict[str, str | int]:
    command = f"find {payload.path} -maxdepth 1 {'-a' if payload.include_hidden else ''} -type f"
    result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=8)
    return {"path": payload.path, "exit_code": result.returncode, "output": result.stdout}
