import pytest

from app.deployment_security import DeploymentSecurity, get_deployment_security


def test_deployment_security_defaults() -> None:
    sec = DeploymentSecurity()
    assert sec.environment == "production"
    assert sec.hardening_enabled is True
    assert sec.enforce_https is True
    assert sec.is_non_root_user is True


def test_security_headers_generation() -> None:
    sec = DeploymentSecurity(environment="production", enforce_https=True)
    headers = sec.get_security_headers()
    assert headers["X-Content-Type-Options"] == "nosniff"
    assert headers["X-Frame-Options"] == "DENY"
    assert "Strict-Transport-Security" in headers
    assert "Content-Security-Policy" in headers


def test_jwt_algorithm_and_expiry_validation() -> None:
    sec = DeploymentSecurity(hardening_enabled=True, max_token_expire_minutes=60)
    
    # Valid parameters
    assert sec.validate_jwt_algorithm_and_expiry("HS256", 30) is True
    
    # Insecure algorithm rejection
    with pytest.raises(ValueError, match="forbidden"):
        sec.validate_jwt_algorithm_and_expiry("none", 30)
        
    # Expiration exceeding threshold
    with pytest.raises(ValueError, match="exceeds maximum allowed threshold"):
        sec.validate_jwt_algorithm_and_expiry("HS256", 120)
        
    # Invalid zero or negative expiry
    with pytest.raises(ValueError, match="must be greater than zero"):
        sec.validate_jwt_algorithm_and_expiry("HS256", 0)


def test_health_status_enrichment() -> None:
    sec = DeploymentSecurity(environment="staging")
    health = sec.get_health_status()
    assert health["status"] == "ok"
    assert health["service"] == "deployguard-risk-lab-api"
    assert health["deployment"]["environment"] == "staging"
    assert health["deployment"]["hardened"] is True


def test_global_get_deployment_security_factory() -> None:
    sec = get_deployment_security()
    assert isinstance(sec, DeploymentSecurity)
