from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from api.routes import api_router
from app.config import get_settings
from app.logging_config import configure_logging
from app.security_headers import SecurityHeadersMiddleware
from app.validation import request_validation_error_handler
from database.session import Base, engine
from middleware.logging import RequestLoggingMiddleware


def create_app() -> FastAPI:
    configure_logging()
    settings = get_settings()
    Base.metadata.create_all(bind=engine)

    app = FastAPI(title=settings.app_name, version="0.1.0")
    app.add_exception_handler(RequestValidationError, request_validation_error_handler)
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RequestLoggingMiddleware)
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