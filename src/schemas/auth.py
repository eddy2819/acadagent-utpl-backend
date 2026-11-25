from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr

from src.enums import UserRole


class RegisterRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "email": "estudiante@example.com",
                "password": "ClaveDePrueba2026!",
                "role": "student",
            }
        },
    )

    email: EmailStr
    password: SecretStr = Field(min_length=8, max_length=128)
    role: UserRole = UserRole.STUDENT


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    password: SecretStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
