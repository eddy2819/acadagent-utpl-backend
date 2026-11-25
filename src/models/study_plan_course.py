from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Numeric,
    Text,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class StudyPlanCourse(Base):
    __tablename__ = "study_plan_courses"

    __table_args__ = (
        UniqueConstraint(
            "study_plan_id",
            "code",
            name="uq_study_plan_courses_study_plan_code",
        ),
        CheckConstraint(
            "hours IS NULL OR hours >= 0",
            name="ck_study_plan_courses_hours_nonnegative",
        ),
        CheckConstraint(
            "credits IS NULL OR credits >= 0",
            name="ck_study_plan_courses_credits_nonnegative",
        ),
        CheckConstraint(
            "length(trim(code)) > 0",
            name="ck_study_plan_courses_code_not_blank",
        ),
        CheckConstraint(
            "length(trim(name)) > 0",
            name="ck_study_plan_courses_name_not_blank",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    study_plan_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey(
            "study_plans.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    code: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    hours: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )

    credits: Mapped[Decimal | None] = mapped_column(
        Numeric,
        nullable=True,
    )
