"""Request-level authentication guard for protected API paths."""

from fastapi import Request
from fastapi.responses import JSONResponse
from jose import JWTError
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import get_settings
from app.request_context import RequestContext, build_request_context
from auth.session import validate_session_token
from auth.user_context import UserContext, build_user_context


class SessionAuthenticationMiddleware(BaseHTTPMiddleware):
    """Reject malformed or invalid bearer sessions before protected handlers run."""

    protected_prefix = "/api/v1/users"

    async def dispatch(self, request: Request, call_next):  # type: ignore[no-untyped-def]
        if not request.url.path.startswith(self.protected_prefix):
            return await call_next(request)

        authorization = request.headers.get("Authorization", "")
        scheme, _, token = authorization.partition(" ")
        if scheme.lower() != "bearer" or not token:
            return JSONResponse(status_code=401, content={"detail": "Not authenticated"})
        try:
            settings = get_settings()
            claims = validate_session_token(token, settings)
            request_context: RequestContext = build_request_context(request, claims)
            request.state.request_context = request_context
            context: UserContext = build_user_context(
                claims, (), cache_seconds=settings.user_context_cache_seconds
            )
            request.state.user_context = context
        except JWTError:
            return JSONResponse(status_code=401, content={"detail": "Could not validate credentials"})
        return await call_next(request)
