from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AuthEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID | None
    event_type: str
    result: str
    reason_code: str | None
    request_id: str | None
    occurred_at: datetime
