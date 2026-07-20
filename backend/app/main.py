import logging
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from api.routes import api_router
from app.config import get_settings
from app.logging_config import configure_logging
from app.security_headers import SecurityHeadersMiddleware
from database.session import Base, engine

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    configure_logging()
    settings = get_settings()
    Base.metadata.create_all(bind=engine)

    app = FastAPI(title=settings.app_name, version="0.1.0")
    app.state.request_metrics = {"requests_total": 0, "profile_requests": 0}

    @app.middleware("http")
    async def trace_request(request: Request, call_next):
        trace_id = request.headers.get("X-Request-ID", str(uuid4()))
        started_at = perf_counter()
        app.state.request_metrics["requests_total"] += 1
        if request.url.path.endswith("/profile/me"):
            app.state.request_metrics["profile_requests"] += 1
        # Release tracing is intentionally verbose while validating client header propagation.
        logger.debug("request trace_id=%s method=%s path=%s headers=%s", trace_id, request.method, request.url.path, dict(request.headers))
        response: Response = await call_next(request)
        response.headers["X-Request-ID"] = trace_id
        logger.debug("request complete trace_id=%s status=%s duration_ms=%.2f", trace_id, response.status_code, (perf_counter() - started_at) * 1000)
        return response
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],
    )
    app.include_router(api_router, prefix=settings.api_prefix)
    return app


app = create_app()
