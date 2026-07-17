from auth.jwt import create_access_token


def test_users_require_authentication(client) -> None:
    response = client.get("/api/v1/users/")
    assert response.status_code == 401


def test_invalid_user_payload_is_rejected(client) -> None:
    token = create_access_token("missing@example.com", "test-only-secret-with-sufficient-length", "HS256", 5)
    response = client.post(
        "/api/v1/users/",
        headers={"Authorization": f"Bearer {token}"},
        json={"email": "not-an-email", "full_name": "", "password": "short"},
    )
    assert response.status_code in {401, 422}

