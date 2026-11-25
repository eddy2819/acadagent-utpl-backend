from decimal import Decimal
from typing import Annotated
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
)

CourseCode = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=50,
    ),
]

CourseName = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=200,
    ),
]

NonNegativeDecimal = Annotated[
    Decimal,
    Field(
        ge=0,
        allow_inf_nan=False,
    ),
]


class StudyPlanCourseCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    study_plan_id: UUID
    code: CourseCode
    name: CourseName
    hours: NonNegativeDecimal | None = None
    credits: NonNegativeDecimal | None = None


class StudyPlanCourseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    study_plan_id: UUID
    code: str
    name: str
    hours: Decimal | None
    credits: Decimal | None
