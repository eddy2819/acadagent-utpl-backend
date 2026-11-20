from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr

from src.models.user import UserRole


class RegisterRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "password": "string",
                "role": "student",
            }
        },
    )

    email: EmailStr
    password: SecretStr = Field(min_length=6, max_length=128)
    role: UserRole


class LoginRequest(BaseModel):
    email: EmailStr
    password: SecretStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
