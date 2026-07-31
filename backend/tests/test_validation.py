def test_validation_errors_do_not_echo_invalid_values(client) -> None:
    response = client.post("/api/v1/auth/login", data={"username": "user@example.com"})

    assert response.status_code == 422
    body = response.json()
    assert body["detail"] == "Request validation failed"
    assert body["errors"]
    assert "user@example.com" not in response.text