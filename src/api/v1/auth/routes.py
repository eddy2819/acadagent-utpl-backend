from fastapi import APIRouter, HTTPException, status

from src.api.dependencies import (
    CurrentUser,
    DatabaseSession,
    unauthorized,
)
from src.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)
from src.schemas.user import UserRead
from src.services.auth.security import create_access_token
from src.services.auth.service import (
    EmailAlreadyRegisteredError,
    authenticate_user,
    create_user,
)

routerAuth = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@routerAuth.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"description": "El correo ya está registrado."},
    },
)
def register(
    data: RegisterRequest,
    session: DatabaseSession,
) -> UserRead:
    try:
        user = create_user(
            session=session,
            email=str(data.email),
            password=data.password.get_secret_value(),
            role=data.role,
        )
    except EmailAlreadyRegisteredError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una cuenta con ese correo.",
        ) from None

    return UserRead.model_validate(user)


@routerAuth.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    data: LoginRequest,
    session: DatabaseSession,
) -> TokenResponse:
    user = authenticate_user(
        session=session,
        email=str(data.email),
        password=data.password.get_secret_value(),
    )

    if user is None:
        raise unauthorized()

    return TokenResponse(
        access_token=create_access_token(user.id),
    )


@routerAuth.get(
    "/me",
    response_model=UserRead,
)
def read_me(user: CurrentUser) -> UserRead:
    return UserRead.model_validate(user)
