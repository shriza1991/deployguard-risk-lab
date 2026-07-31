def test_health_endpoint(client) -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "deployguard-risk-lab-api"
    assert "deployment" in data
    assert data["deployment"]["hardened"] is True
    assert data["deployment"]["non_root"] is True
