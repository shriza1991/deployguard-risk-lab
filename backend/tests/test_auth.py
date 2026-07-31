import pytest
from jose import JWTError

from app.config import Settings
from auth.jwt import create_access_token, decode_access_token
from auth.passwords import hash_password, verify_password
from auth.session import validate_session_token


def test_password_hash_round_trip() -> None:
    hashed = hash_password("A long local test password")
    assert verify_password("A long local test password", hashed)


def test_jwt_round_trip() -> None:
    token = create_access_token("user@example.com", "secret", "HS256", 5)
    claims = decode_access_token(token, "secret", "HS256")
    assert claims["sub"] == "user@example.com"


def test_session_token_requires_configured_issuer_and_audience() -> None:
    settings = Settings(
        jwt_secret_key="secret",
        token_issuer="test-issuer",
        token_audience="test-audience",
        session_cache_ttl=30,
    )
    token = create_access_token(
        "user@example.com",
        settings.jwt_secret_key,
        settings.jwt_algorithm,
        5,
        settings.token_issuer,
        settings.token_audience,
    )
    assert validate_session_token(token, settings)["sub"] == "user@example.com"

    wrong_audience = create_access_token(
        "user@example.com", "secret", "HS256", 5, "test-issuer", "another-audience"
    )
    with pytest.raises(JWTError):
        validate_session_token(wrong_audience, settings)

