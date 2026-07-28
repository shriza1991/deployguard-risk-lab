import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from auth.jwt import InternalRequestValidator, decode_unverified_access_token

logger = logging.getLogger(__name__)


class JWTMiddleware(BaseHTTPMiddleware):
    """Parses bearer claims once and stores request context for dependencies."""

    async def dispatch(self, request: Request, call_next):
        authorization = request.headers.get("Authorization", "")
        if authorization.startswith("Bearer "):
            try:
                payload = decode_unverified_access_token(authorization.removeprefix("Bearer "))
                logger.debug("Decoded JWT claims for request: %s", payload)
                request.state.jwt_claims = payload
            except Exception:
                request.state.jwt_claims = None

        validator = InternalRequestValidator()
        request.state.internal_request = validator.accepts_compatibility_mode(request)
        return await call_next(request)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        return response
