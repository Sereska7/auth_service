"""V1 service layer."""

from dependency_injector import containers, providers

from app.internal.repository import Repositories
from app.internal.repository.v1 import jwt, postgresql, rabbitmq, redis
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

    rabbitmq_repositories: rabbitmq.Repositories = providers.Container(
        Repositories.v1.rabbitmq,
    )  # type: ignore

    postgres_repositories: postgresql.Repositories = providers.Container(
        Repositories.v1.postgres,
    )  # type: ignore

    jwt_repositories: jwt.Repositories = providers.Container(
        Repositories.v1.jwt,
    )  # type: ignore

    clients: Clients = providers.Container(Clients)

    user_service = providers.Factory(UserService)
    user_service.add_attributes(
        user_repository=postgres_repositories.user_repository,
        redis_repository=redis_repositories.base_redis_repository,
        rabbitmq_repository=rabbitmq_repositories.base_rabbitmq_repository,
    )

    auth_service = providers.Factory(AuthService)
    auth_service.add_attributes(
        user_repository=postgres_repositories.user_repository,
        jwt_handler=jwt_repositories.jwt_repository,
    )
