"""
Routes for User module.
"""

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status, Response

from app.internal.pkg.dependencies import get_current_user_from_auth
from app.internal.services import Services
from app.internal.services.v1 import UserService, AuthService
from app.pkg.models import v1 as models
from app.pkg.models.base.request_id_route import RequestIDRoute

router = APIRouter(prefix="/user", tags=["User"], route_class=RequestIDRoute)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=models.UserRegisterResponse,
    description="""
    Description: Create new user.
    Used: Method is used to create user.
    """,
)
@inject
async def register_user(
    cmd: models.UserRegisterCommand,
    user_service: UserService = Depends(Provide[Services.v1.user_service]),
) -> models.UserRegisterResponse:
    return await user_service.register_user(cmd)


@router.patch(
    "/verify",
    status_code=status.HTTP_200_OK,
    response_model=models.TokenResponse,
    description="""
    Description: Verify user email.
    Used: Method is used to confirm a user's email address with a verification code.
    """,
)
@inject
async def verify_code(
    cmd: models.UserVerifyCommand,
    response: Response,
    user_service: UserService = Depends(Provide[Services.v1.user_service]),
    auth_service: AuthService = Depends(Provide[Services.v1.auth_service]),
) -> models.TokenResponse:
    user =  await user_service.verify_user_email(cmd)
    tokens = await auth_service.issue_tokens(user.user_id)
    auth_service.set_token_cookies(
        response=response,
        tokens=tokens
    )
    return tokens



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
