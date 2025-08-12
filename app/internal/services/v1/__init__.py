"""V1 service layer."""

from dependency_injector import containers, providers

from app.internal.pkg.middlewares.verification_email import VerifyEmail
from app.internal.repository import Repositories
from app.internal.repository.v1 import jwt, postgresql, redis
from app.internal.services.v1.auth import AuthService
from app.internal.services.v1.user import UserService
from app.pkg.clients import Clients
from app.pkg.settings import settings


class Services(containers.DeclarativeContainer):
    """Containers with services."""

    configuration = providers.Configuration(name="settings")
    configuration.from_dict(settings.model_dump())

    redis_repositories: redis.RedisRepositories = providers.Container(
        Repositories.v1.redis,
    )  # type: ignore

    postgres_repositories: postgresql.Repositories = providers.Container(
        Repositories.v1.postgres,
    )  # type: ignore

    jwt_repositories: jwt.Repositories = providers.Container(
        Repositories.v1.jwt,
    )

    clients: Clients = providers.Container(Clients)

    verify_email_service = providers.Factory(
        VerifyEmail
    )
    verify_email_service.add_attributes(
        redis_repository=redis_repositories.base_redis_repository
    )

    user_service = providers.Factory(UserService)
    user_service.add_attributes(
        user_repository=postgres_repositories.user_repository,
        verify_email=verify_email_service,
        notification_service_client=clients.v1.notification_service_client,
    )

    auth_service = providers.Factory(AuthService)
    auth_service.add_attributes(
        user_repository=postgres_repositories.user_repository,
        jwt_handler=jwt_repositories.jwt_repository,
    )
