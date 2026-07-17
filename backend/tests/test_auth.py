from auth.jwt import create_access_token, decode_access_token
from auth.passwords import hash_password, verify_password


def test_password_hash_round_trip() -> None:
    hashed = hash_password("A long local test password")
    assert verify_password("A long local test password", hashed)


def test_jwt_round_trip() -> None:
    token = create_access_token("user@example.com", "secret", "HS256", 5)
    claims = decode_access_token(token, "secret", "HS256")
    assert claims["sub"] == "user@example.com"

