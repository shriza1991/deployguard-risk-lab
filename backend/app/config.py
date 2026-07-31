from functools import lru_cache
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.deployment_security import DeploymentSecurity


class DeploymentConfig(BaseModel):
    """
    Infrastructure & runtime deployment parameters.
    """
    app_name: str = Field(default="DeployGuard Risk Lab API", description="Public application identifier")
    environment: str = Field(default="development", description="Deployment environment tier (dev, staging, production)")
    port: int = Field(default=8000, description="Target container listening port")
    api_prefix: str = Field(default="/api/v1", description="Global API routing path prefix")
    log_level: str = Field(default="INFO", description="Application logging level (DEBUG, INFO, WARN, ERROR)")


class SecurityConfig(BaseModel):
    """
    Security-sensitive application and platform parameters.
    """
    # Secret keys must be overridden in non-development environments
    jwt_secret_key: str = Field(default="change-me-in-local-env", description="HMAC key used for signing JWT access tokens")
    jwt_algorithm: str = Field(default="HS256", description="Cryptographic signing algorithm for JWT tokens")
    access_token_expire_minutes: int = Field(default=30, description="Lifetime of issued access tokens in minutes")
    
    # Network and CORS controls
    allowed_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:5173", "http://127.0.0.1:5173", "https://risk-lab.example.com"],
        description="Whitelisted CORS origin URLs allowed to interact with the API",
    )
    
    # Security hardening flags
    hardening_enabled: bool = Field(default=True, description="Enables process non-root execution & strict security rules")
    enforce_https: bool = Field(default=True, description="Enforces HSTS and secure HTTP header posture")


class Settings(BaseSettings):
    """
    Central application settings combining deployment and security configurations.
    """
    app_name: str = "DeployGuard Risk Lab API"
    environment: str = "development"
    port: int = 8000
    api_prefix: str = "/api/v1"
    database_url: str = "sqlite:///./risklab.db"
    jwt_secret_key: str = "change-me-in-local-env"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    allowed_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173", "https://risk-lab.example.com"]
    log_level: str = "INFO"
    security_hardening_enabled: bool = True
    enforce_https: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def deployment_config(self) -> DeploymentConfig:
        return DeploymentConfig(
            app_name=self.app_name,
            environment=self.environment,
            port=self.port,
            api_prefix=self.api_prefix,
            log_level=self.log_level,
        )

    @property
    def security_config(self) -> SecurityConfig:
        return SecurityConfig(
            jwt_secret_key=self.jwt_secret_key,
            jwt_algorithm=self.jwt_algorithm,
            access_token_expire_minutes=self.access_token_expire_minutes,
            allowed_origins=self.allowed_origins,
            hardening_enabled=self.security_hardening_enabled,
            enforce_https=self.enforce_https,
        )

    def get_deployment_security_helper(self) -> DeploymentSecurity:
        return DeploymentSecurity(
            environment=self.environment,
            hardening_enabled=self.security_hardening_enabled,
            enforce_https=self.enforce_https,
            max_token_expire_minutes=60,
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
