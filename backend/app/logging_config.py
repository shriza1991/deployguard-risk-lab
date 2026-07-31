import json
import logging
import sys
from datetime import datetime, timezone

from app.config import get_settings


class JsonFormatter(logging.Formatter):
    """Emit machine-readable logs while retaining a small, safe event schema."""

    def format(self, record: logging.LogRecord) -> str:
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        for field in ("method", "path", "status_code", "duration_ms", "error_count"):
            value = getattr(record, field, None)
            if value is not None:
                event[field] = value
        return json.dumps(event, default=str)


def configure_logging() -> None:
    settings = get_settings()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    logging.basicConfig(
        level=settings.log_level,
        handlers=[handler],
    )

