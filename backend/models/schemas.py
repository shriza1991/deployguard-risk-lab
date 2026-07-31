from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class DeploymentMetadata(BaseModel):
    environment: str = "production"
    hardened: bool = True
    non_root: bool = True


class HealthResponse(BaseModel):
    status: str
    service: str
    deployment: DeploymentMetadata | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=120)
    role: str = Field(default="viewer", pattern="^(admin|editor|viewer)$")


class UserCreate(UserBase):
    password: str = Field(min_length=12, max_length=128)


class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=120)
    role: str | None = Field(default=None, pattern="^(admin|editor|viewer)$")
    is_active: bool | None = None


class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
