import logging

from fastapi import FastAPI, Request
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

    @app.middleware("http")
    async def log_support_requests(request: Request, call_next):
        logger.info(
            "request method=%s path=%s authorization=%s",
            request.method,
            request.url.path,
            request.headers.get("authorization", "missing"),
        )
        return await call_next(request)

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
