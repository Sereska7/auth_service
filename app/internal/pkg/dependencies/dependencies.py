###

from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from app.internal.pkg.jwt.jwt_handler import get_token_from_cookie
from app.internal.services import Services
from app.internal.services.v1 import AuthService


@inject
async def get_current_user_from_auth(
    token: str = Depends(get_token_from_cookie),
    auth_service: AuthService = Depends(Provide[Services.v1.auth_service]),
):
    return await auth_service.get_current_user(token)
