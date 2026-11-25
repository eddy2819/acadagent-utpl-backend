from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class Role(Base):
    __tablename__ = "roles"

    __table_args__ = (
        CheckConstraint(
            "code = lower (trim(code)) AND length(code) > 0",
            name="ck_roles_code_normalized",
        ),
        CheckConstraint(
            "length(trim(name)) > 0",
            name="ck_roles_name_not_black",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    code: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        unique=True,
    )

    name: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
