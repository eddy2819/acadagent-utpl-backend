from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from src.db.session import get_session
from src.models.user import User
from src.services.auth.security import read_access_token

DatabaseSession = Annotated[Session, Depends(get_session)]

bearer_scheme = HTTPBearer(auto_error=False)
BearerCredentials = Annotated[
    HTTPAuthorizationCredentials | None,
    Depends(bearer_scheme),
]


def unauthorized() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_user(
    session: DatabaseSession,
    credentials: BearerCredentials,
) -> User:
    if credentials is None:
        raise unauthorized()

    try:
        user_id = read_access_token(credentials.credentials)
    except (jwt.InvalidTokenError, ValueError):
        raise unauthorized() from None

    user = session.get(User, user_id)
    if user is None or not user.is_active:
        raise unauthorized()

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
