from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, StringConstraints

InstitutionalCode = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=100,
    ),
]

AffiliationType = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=50,
    ),
]


class ApplicantProfileCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    institutional_code: InstitutionalCode | None = None
    affiliation_type: AffiliationType | None = None


class ApplicantProfileUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    institutional_code: InstitutionalCode | None = None
    affiliation_type: AffiliationType | None = None


class ApplicantProfileRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID
    institutional_code: str | None
    affiliation_type: str | None
    updated_at: datetime
