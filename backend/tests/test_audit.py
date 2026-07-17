from services.audit_service import AuditService


def test_audit_event_records_actor_and_target() -> None:
    event = AuditService().record("user.read", "admin@example.com", "user:1")
    assert event.action == "user.read"
    assert event.actor == "admin@example.com"
    assert event.target == "user:1"

