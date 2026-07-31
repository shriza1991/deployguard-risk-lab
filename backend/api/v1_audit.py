from fastapi import APIRouter, Depends

from api.dependencies import get_current_user, get_permission_service
from models.user import User
from services.audit_service import AuditService
from services.permission_service import PermissionService

router = APIRouter()


@router.get("/events/{target}")
def inspect_audit_target(
    target: str,
    current_user: User = Depends(get_current_user),
    permissions: PermissionService = Depends(get_permission_service),
) -> dict[str, str]:
    permissions.require_any_role(current_user, {"admin"})
    event = AuditService().record("audit.inspect", current_user.email, target)
    return {"action": event.action, "actor": event.actor, "target": event.target}
