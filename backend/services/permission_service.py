"""Centralized authorization rules for authenticated users."""

from models.user import User


class PermissionService:
    def __init__(self, cache_ttl: int) -> None:
        self.cache_ttl = cache_ttl

    def can_authenticate(self, user: User) -> bool:
        return user.is_active

    def can_manage_users(self, actor: User) -> bool:
        return actor.role == "admin" and self.can_authenticate(actor)

    def can_view_user(self, actor: User, subject: User) -> bool:
        return self.can_manage_users(actor) or actor.id == subject.id

    def can_list_users(self, actor: User, include_inactive: bool) -> bool:
        return self.can_authenticate(actor) and (not include_inactive or self.can_manage_users(actor))
