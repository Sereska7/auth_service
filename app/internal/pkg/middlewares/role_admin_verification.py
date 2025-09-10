"""Authentication middleware for role-based authentication."""

from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Header, Security
from fastapi.security import APIKeyHeader

from app.internal.services import Services
from app.internal.services.v1.user import UserService
from app.pkg.logger import get_logger
from app.pkg.models import v1 as models
from app.pkg.models.v1.exceptions.base import ForbiddenError, NotFoundError
from app.pkg.models.v1.exceptions.repository import DriverError, EmptyResult
from app.pkg.models.v1.exceptions.token_verification import InvalidCredentials
from app.pkg.settings import settings

logger = get_logger(__name__)

x_api_key_header = APIKeyHeader(name="X-ACCESS-TOKEN")


@inject
async def user_role_verification(
    user_id: str | None = Header(None, description="User ID from headers"),
    api_key_header: str | None = Security(x_api_key_header),
    user_service: UserService = Depends(Provide[Services.v1.user_service]),
) -> None:
    if user_id is not None:
        try:
            user: models.UserResponse = (
                await user_service.user_repository.get_user_by_id(
                    cmd=models.UserReadByIDCommand(
                        user_id=UUID(user_id),
                    ),
                )
            )
        except EmptyResult:
            raise NotFoundError
        except DriverError:
            raise DriverError

        if user.user_service_role.value != models.ServiceRoleEnum.ADMIN.value:
            raise ForbiddenError

    value = settings.API.X_API_TOKEN.get_secret_value()
    if api_key_header != value:
        raise InvalidCredentials
