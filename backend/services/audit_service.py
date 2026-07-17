import logging
from dataclasses import dataclass
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AuditEvent:
    action: str
    actor: str
    target: str
    created_at: datetime


class AuditService:
    def record(self, action: str, actor: str, target: str) -> AuditEvent:
        event = AuditEvent(action=action, actor=actor, target=target, created_at=datetime.now(timezone.utc))
        logger.info("audit_event action=%s actor=%s target=%s", event.action, event.actor, event.target)
        return event

