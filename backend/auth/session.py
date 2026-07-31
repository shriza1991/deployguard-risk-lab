"""Shared validation for bearer tokens used by API dependencies and middleware."""

from datetime import datetime, timedelta, timezone
from threading import Lock
from typing import Any

from jose import JWTError

from app.config import Settings, get_settings
from auth.jwt import decode_access_token

_validation_cache: dict[tuple[str, str, str, str, str], tuple[datetime, dict[str, Any]]] = {}
_cache_lock = Lock()
_MAX_CACHED_SESSIONS = 1_024


def validate_session_token(token: str, settings: Settings | None = None) -> dict[str, Any]:
    """Validate a JWT and return its claims, using a short bounded validation cache.

    Cached entries never outlive either ``SESSION_CACHE_TTL`` or the token expiry.
    """
    settings = settings or get_settings()
    cache_key = (
        token,
        settings.jwt_secret_key,
        settings.jwt_algorithm,
        settings.token_issuer,
        settings.token_audience,
    )
    now = datetime.now(timezone.utc)
    with _cache_lock:
        cached = _validation_cache.get(cache_key)
        if cached and cached[0] > now:
            return cached[1].copy()

    claims = decode_access_token(
        token,
        settings.jwt_secret_key,
        settings.jwt_algorithm,
        issuer=settings.token_issuer,
        audience=settings.token_audience,
    )
    if claims.get("sub") is None:
        raise JWTError("Token subject is required")

    expires_at = datetime.fromtimestamp(claims["exp"], tz=timezone.utc)
    cache_expires_at = min(
        expires_at,
        now + timedelta(seconds=settings.session_cache_ttl),
    )
    with _cache_lock:
        expired_keys = [key for key, (expires, _) in _validation_cache.items() if expires <= now]
        for expired_key in expired_keys:
            del _validation_cache[expired_key]
        if len(_validation_cache) >= _MAX_CACHED_SESSIONS:
            _validation_cache.pop(next(iter(_validation_cache)))
        _validation_cache[cache_key] = (cache_expires_at, claims.copy())
    return claims
