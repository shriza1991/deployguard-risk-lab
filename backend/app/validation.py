import logging

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


async def request_validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Return useful validation feedback without echoing invalid submitted values."""
    logger.info(
        "request_validation_failed",
        extra={"method": request.method, "path": request.url.path, "error_count": len(exc.errors())},
    )
    errors = [
        {"location": list(error["loc"]), "message": error["msg"], "type": error["type"]}
        for error in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Request validation failed", "errors": errors},
    )