import logging
from dataclasses import dataclass
from datetime import datetime, timezone

from app.deployment_security import DeploymentSecurity, get_deployment_security

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AuditEvent:
    action: str
    actor: str
    target: str
    created_at: datetime
    environment: str = "production"


class AuditService:
    def __init__(self, deploy_sec: DeploymentSecurity | None = None) -> None:
        self.deploy_sec = deploy_sec or get_deployment_security()

    def record(self, action: str, actor: str, target: str) -> AuditEvent:
        env = self.deploy_sec.environment
        event = AuditEvent(
            action=action,
            actor=actor,
            target=target,
            created_at=datetime.now(timezone.utc),
            environment=env,
        )
        logger.info(
            "audit_event action=%s actor=%s target=%s env=%s",
            event.action,
            event.actor,
            event.target,
            event.environment,
        )
        return event
