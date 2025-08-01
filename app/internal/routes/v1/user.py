"""Routes for User module."""
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status, Query

from app.internal.pkg.dependencies import get_current_user_from_auth
from app.internal.services import Services
from app.internal.services.v1 import UserService
from app.pkg.models import v1 as models
from app.pkg.models.base.request_id_route import RequestIDRoute

router = APIRouter(prefix="/user", tags=["User"], route_class=RequestIDRoute)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=models.UserResponse,
    description="""
    Description: Create new user.
    Used: Method is used to create user.
    """,
)
@inject
async def register_user(
    cmd: models.UserRegisterCommand,
    user_service: UserService = Depends(Provide[Services.v1.user_service]),
) -> models.UserResponse:
    return await user_service.register_user(cmd)


@router.patch(
    "/change_password",
    status_code=status.HTTP_200_OK,
    description="""
    Description: Changes the password of the currently authenticated user.  
    Used: Method is used when an authenticated user wants to update their password.
    """,
)
@inject
async def change_password(
    cmd: models.UserChangePasswordCommand,
    user_service: UserService = Depends(Provide[Services.v1.user_service]),
    current_user: models.User = Depends(get_current_user_from_auth),
) -> models.UserResponse:
    return await user_service.change_password(
        user=current_user,
        cmd=cmd,
    )


@router.patch(
    "/change_data",
    status_code=status.HTTP_200_OK,
    description="""
    Description: Updates user profile data such as username or email.  
    Used: Allows an authenticated user to modify their personal information.
    """,
)
@inject
async def change_data(
    cmd: models.UserChangeDataCommand,
    user_service: UserService = Depends(Provide[Services.v1.user_service]),
    current_user: models.User = Depends(get_current_user_from_auth),
) -> models.UserResponse:
    return await user_service.change_data(
        cmd=cmd.migrate(
            model=models.UserUpdateDataCommand,
            extra_fields={"user_id": current_user.user_id},
        ),
    )


@router.patch(
    "/verify",
    status_code=status.HTTP_200_OK,
    description="""
    Description: Confirms user verification status by user ID.  
    Used: Called by external services to mark the user as verified after successful confirmation.
    """
)
@inject
async def verify_user(
    user_id: UUID = Query(..., description="User ID for confirmation"),
    user_service: UserService = Depends(Provide[Services.v1.user_service])
):
    await user_service.set_user_verified(user_id)
