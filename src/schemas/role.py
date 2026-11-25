from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, StringConstraints

RoleCode = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        to_lower=True,
        min_length=2,
        max_length=50,
        pattern=r"^[a-z][a-z0-9_]*$",
    ),
]

RoleName = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=2,
        max_length=100,
    ),
]


class RoleCreate(BaseModel):
    """Datos necesarios para crear un rol."""

    model_config = ConfigDict(extra="forbid")

    code: RoleCode
    name: RoleName


class RoleUpdate(BaseModel):
    """Permite cambiar el nombre visible del rol."""

    model_config = ConfigDict(extra="forbid")

    name: RoleName


class RoleRead(BaseModel):
    """Datos del rol que puede devolver la API."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    code: str
    name: str
