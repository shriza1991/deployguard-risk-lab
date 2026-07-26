from datetime import datetime, timedelta, timezone
from jose import jwt


def create_access_token(
    subject: str,
    secret_key: str,
    algorithm: str,
    expires_minutes: int,
    issuer: str,
    audience: str,
) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    claims = {"sub": subject, "exp": expires_at, "iss": issuer, "aud": audience}
    return jwt.encode(claims, secret_key, algorithm=algorithm)
