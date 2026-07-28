import logging

from fastapi import Request
from jose import JWTError
from starlette.middleware.base import BaseHTTPMiddleware

from auth.jwt import decode_unverified_access_token

logger = logging.getLogger(__name__)


class JWTMiddleware(BaseHTTPMiddleware):
    """Adds JWT request context before route-level authorization runs."""

    async def dispatch(self, request: Request, call_next):  # type: ignore[no-untyped-def]
        authorization = request.headers.get("Authorization", "")
        if authorization.startswith("Bearer "):
            try:
                payload = decode_unverified_access_token(authorization.removeprefix("Bearer "))
                logger.debug("Decoded JWT payload for request: %s", payload)
                request.state.jwt_payload = payload
            except JWTError:
                request.state.jwt_payload = None

        request.state.internal_auth_bypass = request.headers.get("X-Internal-Request") == "true"
        return await call_next(request)
