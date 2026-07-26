import logging
from dataclasses import dataclass
from datetime import datetime, timezone

from app.logging_config import get_request_context_log_level
from app.request_context import RequestContext

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AuditEvent:
    action: str
    actor: str
    target: str
    created_at: datetime
    correlation_id: str | None = None


class AuditService:
    def record(self, action: str, actor: str, target: str, context: RequestContext | None = None) -> AuditEvent:
        event = AuditEvent(
            action=action,
            actor=actor,
            target=target,
            created_at=datetime.now(timezone.utc),
            correlation_id=context.correlation_id if context else None,
        )
        logger.log(
            get_request_context_log_level(),
            "audit_event action=%s actor=%s target=%s correlation_id=%s",
            event.action,
            event.actor,
            event.target,
            event.correlation_id,
        )
        return event
