from fastapi import Request, status
from fastapi.responses import JSONResponse
from jose import JWTError
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import Settings
from auth.session import validate_session_token


class SessionAuthenticationMiddleware(BaseHTTPMiddleware):
    """Reject malformed or invalid bearer tokens before protected routes run."""

    def __init__(self, app, settings: Settings) -> None:
        super().__init__(app)
        self.settings = settings
        self.public_paths = {
            f"{settings.api_prefix}/health",
            f"{settings.api_prefix}/auth/login",
            "/docs",
            "/openapi.json",
        }

    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.public_paths or not request.url.path.startswith(self.settings.api_prefix):
            return await call_next(request)

        scheme, _, token = request.headers.get("Authorization", "").partition(" ")
        if scheme.lower() != "bearer" or not token:
            return self._unauthorized_response()
        try:
            validate_session_token(token, self.settings)
        except (JWTError, KeyError, TypeError, ValueError):
            return self._unauthorized_response()
        return await call_next(request)

    @staticmethod
    def _unauthorized_response() -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Could not validate credentials"},
            headers={"WWW-Authenticate": "Bearer"},
        )
