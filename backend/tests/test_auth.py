import pytest
from jose import JWTError

from app.config import Settings
from auth.jwt import create_access_token
from auth.session import validate_session_token
from auth.user_context import UserContext, build_user_context
from auth.passwords import hash_password, verify_password


def test_password_hash_round_trip() -> None:
    hashed = hash_password("A long local test password")
    assert verify_password("A long local test password", hashed)


def test_jwt_round_trip() -> None:
    settings = Settings(jwt_secret_key="secret", token_issuer="tests", token_audience="test-client")
    token = create_access_token(
        "user@example.com",
        settings.jwt_secret_key,
        settings.jwt_algorithm,
        5,
        settings.token_issuer,
        settings.token_audience,
    )
    claims = validate_session_token(token, settings)
    assert claims["sub"] == "user@example.com"


def test_session_token_rejects_wrong_audience() -> None:
    settings = Settings(jwt_secret_key="secret", token_issuer="tests", token_audience="test-client")
    token = create_access_token("user@example.com", "secret", "HS256", 5, "tests", "other-client")
    with pytest.raises(JWTError):
        validate_session_token(token, settings)


def test_build_user_context_uses_a_stable_permission_order() -> None:
    context = build_user_context({"sub": "user@example.com", "role": "admin"}, {"users:manage", "profile:read"}, 45)
    assert isinstance(context, UserContext)
    assert context.permissions == ("profile:read", "users:manage")
    assert context.context_version == "v1"
