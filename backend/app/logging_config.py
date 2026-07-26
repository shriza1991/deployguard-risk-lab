import logging
import sys

from app.config import get_settings


def configure_logging() -> None:
    settings = get_settings()
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def get_request_context_log_level() -> int:
    """Resolve the separate correlation-event log level safely."""
    configured_level = get_settings().request_context_log_level.upper()
    return getattr(logging, configured_level, logging.INFO)
