from fastapi import APIRouter

from src.api.dependencies import CurrentUser, DatabaseSession, unauthorized
from src.schemas.auth import LoginRequest, TokenResponse
from src.schemas.user import UserRead
from src.services.auth.security import create_access_token
from src.services.auth.service import authenticate_user

routerAuth = APIRouter(prefix="/auth", tags=["Authentication"])


@routerAuth.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, session: DatabaseSession) -> TokenResponse:
    user = authenticate_user(
        session=session,
        email=str(data.email),
        password=data.password.get_secret_value(),
    )

    if user is None:
        raise unauthorized()

    return TokenResponse(access_token=create_access_token(user.id))


@routerAuth.get("/me", response_model=UserRead)
def read_me(user: CurrentUser) -> UserRead:
    return UserRead.model_validate(user)
