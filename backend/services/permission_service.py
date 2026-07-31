from collections.abc import Collection

from fastapi import HTTPException, status

from models.user import User


class PermissionService:
    """Centralizes role checks so routes apply authorization consistently."""

    def require_any_role(self, user: User, allowed_roles: Collection[str]) -> User:
        if user.role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return user
