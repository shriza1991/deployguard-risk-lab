import logging


def test_request_logging_records_safe_request_metadata(client, caplog) -> None:
    with caplog.at_level(logging.INFO, logger="middleware.logging"):
        response = client.get("/api/v1/health")

    record = next(record for record in caplog.records if record.message == "request_completed")
    assert response.status_code == 200
    assert record.method == "GET"
    assert record.path == "/api/v1/health"
    assert record.status_code == 200
    assert not hasattr(record, "headers")
    assert not hasattr(record, "body")