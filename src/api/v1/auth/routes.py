from fastapi import APIRouter, HTTPException, status

from src.api.dependencies import (
    BearerCredentials,
    CurrentUser,
    DatabaseSession,
    get_current_user,
    unauthorized,
)
from src.enums import UserRole
from src.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)
from src.schemas.user import UserRead
from src.services.auth.security import create_access_token
from src.services.auth.service import (
    EmailAlreadyRegisteredError,
    RoleAssignmentForbiddenError,
    RoleNotConfiguredError,
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
        401: {"description": "Se requiere autenticación."},
        403: {"description": "No tienes permiso para asignar ese rol."},
        409: {"description": "El correo ya está registrado."},
        503: {"description": "El catálogo de roles no está configurado."},
    },
)
def register(
    data: RegisterRequest,
    session: DatabaseSession,
    credentials: BearerCredentials,
) -> UserRead:
    actor = None

    if credentials is not None or data.role != UserRole.STUDENT:
        actor = get_current_user(
            session=session,
            credentials=credentials,
        )

    try:
        user = create_user(
            session=session,
            email=str(data.email),
            password=data.password.get_secret_value(),
            role=data.role,
            actor=actor,
        )

    except EmailAlreadyRegisteredError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una cuenta con ese correo.",
        ) from None

    except RoleAssignmentForbiddenError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo un administrador puede asignar ese rol.",
        ) from None

    except RoleNotConfiguredError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="El catálogo de roles no está configurado.",
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
