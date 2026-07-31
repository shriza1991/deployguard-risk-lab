from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.deployment_security import get_deployment_security


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware applying hardened HTTP security headers defined by the DeploymentSecurity helper.
    """

    def __init__(self, app, deployment_security=None) -> None:
        super().__init__(app)
        self.deployment_security = deployment_security or get_deployment_security()

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        security_headers = self.deployment_security.get_security_headers()
        for header, value in security_headers.items():
            response.headers[header] = value
        return response
