from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt


def create_access_token(
    subject: str,
    secret_key: str,
    algorithm: str,
    expires_minutes: int,
    issuer: str | None = None,
    audience: str | None = None,
) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    claims = {"sub": subject, "exp": expires_at}
    if issuer:
        claims["iss"] = issuer
    if audience:
        claims["aud"] = audience
    return jwt.encode(claims, secret_key, algorithm=algorithm)


def decode_access_token(
    token: str,
    secret_key: str,
    algorithm: str,
    issuer: str | None = None,
    audience: str | None = None,
) -> dict[str, Any]:
    return jwt.decode(
        token,
        secret_key,
        algorithms=[algorithm],
        issuer=issuer,
        audience=audience,
        options={"require_exp": True},
    )

