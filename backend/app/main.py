from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import api_router
from app.config import get_settings
from app.logging_config import configure_logging
from app.security_headers import SecurityHeadersMiddleware
from database.session import Base, engine


def create_app() -> FastAPI:
    configure_logging()
    settings = get_settings()
    deploy_sec = settings.get_deployment_security_helper()

    # Log deployment posture during app startup
    posture = deploy_sec.verify_runtime_posture()
    Base.metadata.create_all(bind=engine)

    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description=f"DeployGuard Risk Lab API ({posture['environment']} posture)",
    )
    
    # Store deployment security instance in app state
    app.state.deployment_security = deploy_sec

    app.add_middleware(SecurityHeadersMiddleware, deployment_security=deploy_sec)
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
