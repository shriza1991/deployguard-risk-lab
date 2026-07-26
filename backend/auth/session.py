"""Shared session-token validation for API dependencies and middleware."""

from typing import Any

from jose import jwt

from app.config import Settings


def validate_session_token(token: str, settings: Settings) -> dict[str, Any]:
    """Decode a bearer token and enforce the claims issued by this service.

    ``JWTError`` is deliberately allowed to propagate so callers can turn an
    invalid session into the appropriate HTTP response without accepting it.
    """
    return jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
        issuer=settings.token_issuer,
        audience=settings.token_audience,
        options={"require_exp": True, "require_sub": True},
    )
