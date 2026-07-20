from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class HealthResponse(BaseModel):
    status: str
    service: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    setup_required: bool = Field(default=False)


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


class ProfileUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=120)
    profile_timezone: str | None = Field(default=None, max_length=64)


class ProfileRead(UserRead):
    # Included for release support while profile synchronization is being validated.
    profile_timezone: str | None = None
