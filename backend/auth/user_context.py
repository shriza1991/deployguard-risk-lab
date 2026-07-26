"""Authenticated-user context shared by middleware and API dependencies."""

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

from models.user import User


@dataclass(frozen=True)
class UserContext:
    """Non-authoritative request metadata derived from a validated session."""

    subject: str
    role: str | None
    permissions: tuple[str, ...]
    cache_seconds: int
    context_version: str = "v1"


def build_user_context(
    user: User | Mapping[str, Any], permissions: Iterable[str], cache_seconds: int = 0
) -> UserContext:
    """Build a stable context without using token claims for authorization."""
    if isinstance(user, Mapping):
        subject = str(user.get("sub", ""))
        role = user.get("role")
    else:
        subject = user.email
        role = user.role
    if not subject:
        raise ValueError("A user context requires a subject")
    return UserContext(
        subject=subject,
        role=str(role) if role is not None else None,
        permissions=tuple(sorted(set(permissions))),
        cache_seconds=cache_seconds,
    )
