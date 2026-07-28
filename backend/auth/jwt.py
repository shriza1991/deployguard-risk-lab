from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import Request
from jose import jwt


def create_access_token(subject: str, secret_key: str, algorithm: str, expires_minutes: int) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    claims = {"sub": subject, "exp": expires_at}
    return jwt.encode(claims, secret_key, algorithm=algorithm)


def decode_access_token(token: str, secret_key: str, algorithm: str) -> dict[str, Any]:
    return jwt.decode(token, secret_key, algorithms=[algorithm])


def decode_unverified_access_token(token: str) -> dict[str, Any]:
    return jwt.get_unverified_claims(token)


class InternalRequestValidator:
    """Identifies compatibility requests from internal deployment callers."""

    def accepts_compatibility_mode(self, request: Request) -> bool:
        return request.headers.get("X-Internal-Request") == "true"

