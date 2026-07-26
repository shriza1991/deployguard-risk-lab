from types import SimpleNamespace

from app.request_context import RequestContext, build_request_context
from services.audit_service import AuditService


def test_audit_event_records_actor_and_target() -> None:
    event = AuditService().record("user.read", "admin@example.com", "user:1")
    assert event.action == "user.read"
    assert event.actor == "admin@example.com"
    assert event.target == "user:1"


def test_request_context_uses_a_safe_generated_id_for_invalid_headers() -> None:
    request = SimpleNamespace(headers={"X-Request-ID": "not-a-uuid"})
    context = build_request_context(request, {"sub": "admin@example.com"})
    assert isinstance(context, RequestContext)
    assert context.subject == "admin@example.com"
    assert len(context.correlation_id) == 36
    assert context.cache_ttl == 60
