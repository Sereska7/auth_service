"""
Routes for Auth module.
"""

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status

from app.internal.services import Services
from app.internal.services.v1 import AuthService
from app.pkg.models import v1 as models
from app.pkg.models.base.request_id_route import RequestIDRoute

router = APIRouter(prefix="/auth", tags=["Auth"], route_class=RequestIDRoute)


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=models.TokenResponse,
    description="""
    Description: Authenticates the user and issues access and refresh tokens.
    Usage: This endpoint logs in the user by validating credentials and setting token cookies.
    """,
)
@inject
async def login(
    cmd: models.AuthCommand,
    response: Response,
    auth_service: AuthService = Depends(Provide[Services.v1.auth_service]),
) -> models.TokenResponse:
    tokens = await auth_service.authenticate_user(cmd)

    response.set_cookie(
        key="access_token",
        value=tokens.access_token,
        httponly=True,
        max_age=3600,
        secure=True,
        samesite="lax",
    )

    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        max_age=14 * 24 * 3600,
        secure=True,
        samesite="lax",
    )

    return tokens


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    description="""
    Description: Refreshes the access and refresh tokens using the refresh token cookie.
    Usage: Issues new tokens to the user if the provided refresh token is valid.
    """,
)
@inject
async def logout(
    response: Response,
) -> dict:
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,
        samesite="lax",
    )
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return {"msg": "Successfully logged out"}


@router.post(
    "/refresh",
    status_code=status.HTTP_200_OK,
    response_model=models.TokenResponse,
    description="""
    Description: Refreshes the access and refresh tokens using the refresh token cookie.
    Usage: Issues new tokens to the user if the provided refresh token is valid.
    """,
)
@inject
async def refresh_tokens(
    response: Response,
    refresh_token: str = Cookie(..., include_in_schema=False),
    auth_service: AuthService = Depends(Provide[Services.v1.auth_service]),
) -> models.TokenResponse:

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    tokens = await auth_service.refresh_access_token(refresh_token)

    response.set_cookie(
        key="access_token",
        value=tokens.access_token,
        httponly=True,
        max_age=3600,
        secure=True,
        samesite="lax",
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        max_age=14 * 24 * 3600,
        secure=True,
        samesite="lax",
    )

    return tokens
