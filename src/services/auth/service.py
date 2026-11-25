from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.enums import UserRole
from src.models.auth_event import AuthEvent
from src.models.role import Role
from src.models.user import User
from src.models.user_role import UserRoleAssignment
from src.services.auth.security import (
    DUMMY_HASH,
    hash_password,
    verify_password,
)


class EmailAlreadyRegisteredError(Exception):
    pass


class RoleNotConfiguredError(Exception):
    pass


class RoleAssignmentForbiddenError(Exception):
    pass


def normalize_email(email: str) -> str:
    return email.strip().lower()


def user_has_role(
    session: Session,
    user: User,
    role_code: str,
) -> bool:
    if not user.is_active:
        return False

    role_id = session.scalar(
        select(Role.id)
        .join(
            UserRoleAssignment,
            UserRoleAssignment.role_id == Role.id,
        )
        .where(
            UserRoleAssignment.user_id == user.id,
            Role.code == role_code,
        )
    )

    return role_id is not None


def authenticate_user(
    session: Session,
    email: str,
    password: str,
) -> User | None:
    user = session.scalar(
        select(User).where(
            User.email == normalize_email(email),
        )
    )

    stored_hash = user.password_hash if user is not None else DUMMY_HASH

    password_is_valid = verify_password(
        password,
        stored_hash,
    )

    authenticated = user is not None and password_is_valid and user.is_active

    session.add(
        AuthEvent(
            user_id=user.id if user is not None else None,
            event_type="login",
            result="success" if authenticated else "failure",
            reason_code=None if authenticated else "invalid_credentials",
        )
    )

    try:
        session.commit()
    except Exception:
        session.rollback()
        raise

    return user if authenticated else None


def create_user(
    session: Session,
    email: str,
    password: str,
    role: UserRole,
    actor: User | None = None,
) -> User:
    role_code = role.value

    if role != UserRole.STUDENT and (
        actor is None or not user_has_role(
            session,
            actor,
            UserRole.SYSTEM_ADMIN.value,
        )
    ):
        raise RoleAssignmentForbiddenError()

    role_record = session.scalar(select(Role).where(Role.code == role_code))

    if role_record is None:
        raise RoleNotConfiguredError(role_code)

    normalized_email = normalize_email(email)

    user = User(
        email=normalized_email,
        password_hash=hash_password(password),
        is_active=True,
    )

    try:
        session.add(user)
        session.flush()

        session.add(
            UserRoleAssignment(
                user_id=user.id,
                role_id=role_record.id,
                assigned_by=actor.id if actor is not None else None,
            )
        )

        session.add(
            AuthEvent(
                user_id=user.id,
                event_type="register",
                result="success",
            )
        )

        session.commit()

    except IntegrityError:
        session.rollback()

        existing_id = session.scalar(
            select(User.id).where(
                User.email == normalized_email,
            )
        )

        if existing_id is not None:
            raise EmailAlreadyRegisteredError(normalized_email) from None

        raise

    except Exception:
        session.rollback()
        raise

    session.refresh(user)
    return user
