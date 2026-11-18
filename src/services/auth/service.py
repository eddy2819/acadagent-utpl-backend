from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.models.user import User, UserRole
from src.services.auth.security import DUMMY_HASH, hash_password, verify_password


class EmailAlreadyRegisteredError(Exception):
    pass


def normalize_email(email: str) -> str:
    return email.strip().lower()


def authenticate_user(
    session: Session,
    email: str,
    password: str,
) -> User | None:
    user = session.scalar(select(User).where(User.email == normalize_email(email)))

    stored_hash = user.password_hash if user is not None else DUMMY_HASH
    password_is_valid = verify_password(password, stored_hash)

    if user is None or not password_is_valid or not user.is_active:
        return None

    return user


def create_user(
    session: Session,
    email: str,
    password: str,
    role: UserRole,
) -> User:
    normalized_email = normalize_email(email)
    user = User(
        email=normalized_email,
        password_hash=hash_password(password),
        role=role,
        is_active=True,
    )
    session.add(user)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        existing_id = session.scalar(
            select(User.id).where(User.email == normalized_email)
        )
        if existing_id is not None:
            raise EmailAlreadyRegisteredError(normalized_email) from None
        raise

    session.refresh(user)
    return user
