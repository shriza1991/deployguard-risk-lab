from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt

from app.deployment_security import get_deployment_security


def create_access_token(subject: str, secret_key: str, algorithm: str, expires_minutes: int) -> str:
    sec = get_deployment_security()
    sec.validate_jwt_algorithm_and_expiry(algorithm, expires_minutes)
    
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    claims = {"sub": subject, "exp": expires_at}
    return jwt.encode(claims, secret_key, algorithm=algorithm)


def decode_access_token(token: str, secret_key: str, algorithm: str) -> dict[str, Any]:
    sec = get_deployment_security()
    sec.validate_jwt_algorithm_and_expiry(algorithm, 1)  # validate algorithm policy
    return jwt.decode(token, secret_key, algorithms=[algorithm])
