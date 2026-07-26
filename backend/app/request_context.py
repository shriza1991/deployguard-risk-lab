"""Safe request-correlation metadata for logs and audit events."""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any
from uuid import UUID, uuid4

from fastapi import Request

from app.config import get_settings
from models.user import User


@dataclass(frozen=True)
class RequestContext:
    correlation_id: str
    subject: str | None
    cache_ttl: int


def build_request_context(request: Request, user: User | Mapping[str, Any] | None) -> RequestContext:
    """Return a canonical correlation ID without trusting arbitrary header text."""
    supplied_id = request.headers.get("X-Request-ID")
    try:
        correlation_id = str(UUID(supplied_id)) if supplied_id else str(uuid4())
    except ValueError:
        correlation_id = str(uuid4())

    if isinstance(user, Mapping):
        subject = user.get("sub")
    else:
        subject = user.email if user is not None else None
    return RequestContext(
        correlation_id=correlation_id,
        subject=str(subject) if subject else None,
        cache_ttl=get_settings().request_context_cache_ttl,
    )
