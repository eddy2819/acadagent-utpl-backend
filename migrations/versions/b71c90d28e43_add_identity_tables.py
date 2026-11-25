"""Add identity tables and migrate existing user roles."""

from uuid import uuid4

import sqlalchemy as sa
from alembic import op

revision = "b71c90d28e43"
down_revision = "8db3bdeba2d0"
branch_labels = None
depends_on = None


ROLE_CATALOG = (
    ("system_admin", "Administrador del sistema"),
    ("student", "Estudiante / solicitante"),
    ("secretary", "Secretaría"),
    ("evaluator", "Evaluador"),
    ("program_director", "Director de carrera"),
    ("quality_team", "Equipo de calidad"),
    ("coordinator", "Coordinador"),
    ("faculty_reviewer", "Docente revisor"),
)


def upgrade() -> None:
    op.create_table(
        "roles",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.Text(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
        sa.CheckConstraint(
            "code = lower(trim(code)) AND length(code) > 0",
            name="ck_roles_code_normalized",
        ),
        sa.CheckConstraint(
            "length(trim(name)) > 0",
            name="ck_roles_name_not_blank",
        ),
    )

    op.create_table(
        "user_roles",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("role_id", sa.Uuid(), nullable=False),
        sa.Column("assigned_by", sa.Uuid(), nullable=True),
        sa.Column(
            "assigned_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("user_id", "role_id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["assigned_by"], ["users.id"], ondelete="RESTRICT"),
    )

    op.create_index(
        "ix_user_roles_role_id",
        "user_roles",
        ["role_id"],
    )

    op.create_index(
        "ix_user_roles_assigned_by",
        "user_roles",
        ["assigned_by"],
    )

    op.create_table(
        "applicant_profiles",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("institutional_code", sa.Text(), nullable=True),
        sa.Column("affiliation_type", sa.Text(), nullable=True),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("user_id"),
        sa.UniqueConstraint("institutional_code"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="RESTRICT"),
    )

    op.create_table(
        "auth_events",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=True),
        sa.Column("event_type", sa.Text(), nullable=False),
        sa.Column("result", sa.Text(), nullable=False),
        sa.Column("reason_code", sa.Text(), nullable=True),
        sa.Column("request_id", sa.Text(), nullable=True),
        sa.Column(
            "occurred_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="RESTRICT"),
    )

    op.create_index(
        "ix_auth_events_user_id",
        "auth_events",
        ["user_id"],
    )

    op.create_index(
        "ix_auth_events_occurred_at",
        "auth_events",
        ["occurred_at"],
    )

    roles_table = sa.table(
        "roles",
        sa.column("id", sa.Uuid()),
        sa.column("code", sa.Text()),
        sa.column("name", sa.Text()),
    )

    op.bulk_insert(
        roles_table,
        [
            {
                "id": uuid4(),
                "code": code,
                "name": name,
            }
            for code, name in ROLE_CATALOG
        ],
    )

    # Copiar el rol actual de cada cuenta.
    # La fecha corresponde a la migración: no conocemos la
    # fecha original de asignación del rol.
    op.execute(
        sa.text(
            """
            INSERT INTO user_roles (
                user_id,
                role_id,
                assigned_by,
                assigned_at
            )
            SELECT
                users.id,
                roles.id,
                NULL,
                CURRENT_TIMESTAMP
            FROM users
            JOIN roles ON roles.code = users.role
            """
        )
    )

    connection = op.get_bind()

    missing_assignments = connection.scalar(
        sa.text(
            """
            SELECT count(*)
            FROM users
            WHERE NOT EXISTS (
                SELECT 1
                FROM user_roles
                WHERE user_roles.user_id = users.id
            )
            """
        )
    )

    if missing_assignments:
        raise RuntimeError(
            "Hay usuarios cuyo rol no pudo migrarse. Se cancela la migración."
        )

    op.drop_constraint(
        "user_role",
        "users",
        type_="check",
    )

    op.drop_column("users", "role")


def downgrade() -> None:
    raise RuntimeError(
        "Esta migración no admite downgrade automático: "
        "el modelo anterior solo permite un rol por usuario. "
        "La reversión requiere una migración de datos específica."
    )
