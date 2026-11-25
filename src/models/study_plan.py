from datetime import date
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    Date,
    Text,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class StudyPlan(Base):
    __tablename__ = "study_plans"

    __table_args__ = (
        UniqueConstraint(
            "program_code",
            "version",
            name="uq_study_plans_program_version",
        ),
        CheckConstraint(
            "valid_until IS NULL OR valid_until >= valid_from",
            name="ck_study_plans_validity",
        ),
        CheckConstraint(
            "length(trim(program_code)) > 0",
            name="ck_study_plans_program_code_not_blank",
        ),
        CheckConstraint(
            "length(trim(program_name)) > 0",
            name="ck_study_plans_program_name_not_blank",
        ),
        CheckConstraint(
            "length(trim(version)) > 0",
            name="ck_study_plans_version_not_blank",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    program_code: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    program_name: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    version: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    valid_from: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    valid_until: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )
