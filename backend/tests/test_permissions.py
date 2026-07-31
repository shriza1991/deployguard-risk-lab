from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from services.permission_service import PermissionService


def test_permission_service_rejects_disallowed_role() -> None:
    viewer = SimpleNamespace(role="viewer")
    with pytest.raises(HTTPException) as exc_info:
        PermissionService().require_any_role(viewer, {"admin"})
    assert exc_info.value.status_code == 403
