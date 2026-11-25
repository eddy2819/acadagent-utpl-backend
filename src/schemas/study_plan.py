from datetime import date
from typing import Annotated, Self
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    StringConstraints,
    model_validator,
)

ProgramCode = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=50,
    ),
]

ProgramName = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=200,
    ),
]

StudyPlanVersion = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=50,
    ),
]


class StudyPlanCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    program_code: ProgramCode
    program_name: ProgramName
    version: StudyPlanVersion
    valid_from: date
    valid_until: date | None = None

    @model_validator(mode="after")
    def validate_validity(self) -> Self:
        if self.valid_until is not None and self.valid_until < self.valid_from:
            raise ValueError("valid_until must be greater than or equal to valid_from.")

        return self


class StudyPlanRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    program_code: str
    program_name: str
    version: str
    valid_from: date
    valid_until: date | None
