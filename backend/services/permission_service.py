from models.user import User


class PermissionService:
    """Resolves role permissions and retains them for the lifetime of the process."""

    _role_permissions = {
        "admin": frozenset({"users:read", "users:write"}),
        "editor": frozenset({"users:read"}),
        "viewer": frozenset({"users:read"}),
    }

    def __init__(self) -> None:
        self._permission_cache: dict[str, frozenset[str]] = {}

    def permissions_for(self, user: User) -> frozenset[str]:
        if user.role not in self._permission_cache:
            self._permission_cache[user.role] = self._role_permissions.get(user.role, frozenset())
        return self._permission_cache[user.role]

    def can(self, user: User, permission: str) -> bool:
        return permission in self.permissions_for(user)
