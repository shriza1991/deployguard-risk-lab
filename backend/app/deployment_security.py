import os
import sys
from typing import Any


class DeploymentSecurity:
    """
    Shared deployment security helper providing container runtime posture checks,
    security headers management, probe readiness validation, and token policy enforcement.
    """

    DEFAULT_SECURITY_HEADERS: dict[str, str] = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Content-Security-Policy": "default-src 'self'; frame-ancestors 'none'; object-src 'none';",
        "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
    }

    def __init__(
        self,
        environment: str = "production",
        hardening_enabled: bool = True,
        enforce_https: bool = True,
        max_token_expire_minutes: int = 60,
    ) -> None:
        self.environment = environment
        self.hardening_enabled = hardening_enabled
        self.enforce_https = enforce_https
        self.max_token_expire_minutes = max_token_expire_minutes

    @property
    def is_non_root_user(self) -> bool:
        """
        Returns True if the current process is running as a non-root user (UID != 0)
        or on non-POSIX systems like Windows (where getuid is unavailable).
        """
        if hasattr(os, "getuid"):
            return os.getuid() != 0  # type: ignore[attr-defined]
        return True

    def get_security_headers(self) -> dict[str, str]:
        """
        Generates standard HTTP security headers tailored to the active deployment posture.
        """
        headers = dict(self.DEFAULT_SECURITY_HEADERS)
        if self.enforce_https or self.environment == "production":
            headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
        return headers

    def verify_runtime_posture(self) -> dict[str, Any]:
        """
        Evaluates current deployment runtime security posture.
        """
        return {
            "environment": self.environment,
            "hardening_enabled": self.hardening_enabled,
            "non_root_execution": self.is_non_root_user,
            "https_enforced": self.enforce_https,
            "python_version": sys.version.split()[0],
        }

    def validate_jwt_algorithm_and_expiry(self, algorithm: str, expire_minutes: int) -> bool:
        """
        Validates JWT signing algorithm and expiration parameters against security baseline policies.
        Reject weak algorithms like 'none' and excessively long expiration times in production.
        """
        if algorithm.lower() == "none":
            raise ValueError("Insecure JWT algorithm 'none' is forbidden in deployment baseline.")
        if expire_minutes <= 0:
            raise ValueError("Token expiration minutes must be greater than zero.")
        if self.hardening_enabled and expire_minutes > self.max_token_expire_minutes:
            raise ValueError(
                f"Token expiration ({expire_minutes}m) exceeds maximum allowed threshold ({self.max_token_expire_minutes}m)."
            )
        return True

    def get_health_status(self) -> dict[str, Any]:
        """
        Enriches health probe responses with deployment security metadata.
        """
        posture = self.verify_runtime_posture()
        return {
            "status": "ok",
            "service": "deployguard-risk-lab-api",
            "deployment": {
                "environment": self.environment,
                "hardened": posture["hardening_enabled"],
                "non_root": posture["non_root_execution"],
            },
        }


# Global default instance initialized with environment overrides
def get_deployment_security() -> DeploymentSecurity:
    env = os.getenv("ENVIRONMENT", "production")
    hardening = os.getenv("SECURITY_HARDENING_ENABLED", "true").lower() == "true"
    https = os.getenv("ENFORCE_HTTPS", "true").lower() == "true"
    max_expire = int(os.getenv("MAX_TOKEN_EXPIRE_MINUTES", "60"))
    return DeploymentSecurity(
        environment=env,
        hardening_enabled=hardening,
        enforce_https=https,
        max_token_expire_minutes=max_expire,
    )
