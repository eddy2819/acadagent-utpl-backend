from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserRoleAssign(BaseModel):
    model_config = ConfigDict(extra="forbid")

    role_id: UUID


class UserRoleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID
    role_id: UUID
    assigned_by: UUID | None
    assigned_at: datetime
